from __future__ import division, print_function
import os, re, time, csv, sys
from io_util import make_dir, remove_dir, write_json
# from io_util import myopen, make_dir, remove_dir, tree_to_json, write_json
# from collections import defaultdict
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import generic_dna
from Bio.SeqFeature import FeatureLocation
import numpy as np
from seq_util import pad_nucleotide_sequences, nuc_alpha, aa_alpha
from datetime import datetime
import json
from pdb import set_trace
from utils import fix_names, num_date, parse_date
from pprint import pprint
from Bio import AlignIO
from Bio.Align import MultipleSeqAlignment
import random

TINY = 1e-10

def calc_af(aln, alpha):
    aln_array = np.array(aln)
    af = np.zeros((len(alpha), aln_array.shape[1]))
    for ai, state in enumerate(alpha):
        af[ai] += (aln_array==state).mean(axis=0)
    af[-1] = 1.0 - af[:-1].sum(axis=0)
    return af

class sequence_set(object):

    def __init__(self, logger, sequences, reference, dateFormat):
        super(sequence_set, self).__init__()
        self.log = logger

        # load sequences from the (parsed) JSON - don't forget to sort out dates
        self.seqs = {}
        for name, data in sequences.iteritems():
            self.seqs[name] = SeqRecord(Seq(data["seq"], generic_dna),
                   id=name, name=name, description=name)
            self.seqs[name].attributes = data["attributes"]
            # tidy up dates
            date_struc = parse_date(self.seqs[name].attributes["raw_date"], dateFormat)
            self.seqs[name].attributes["num_date"] = date_struc[1]
            self.seqs[name].attributes["date"] = date_struc[2]

        # if the reference is to be analysed it'll already be in the (filtered & subsampled)
        # sequences, so no need to add it here, and no need to care about attributes etc
        # we do, however, need it for alignment
        self.reference_in_dataset = reference["included"]
        name = reference["strain"]
        self.reference_seq = SeqRecord(Seq(reference["seq"], generic_dna),
               id=name, name=name, description=name)
        if "genes" in reference and len(reference["genes"]):
            self.proteins = {k:FeatureLocation(start=v["start"], end=v["end"], strand=v["strand"]) for k, v in reference["genes"].iteritems()}
        else:
            self.proteins = None

        # other things:
        self.run_dir = '_'.join(['temp', time.strftime('%Y%m%d-%H%M%S',time.gmtime()), str(random.randint(0,1000000))])
        self.nthreads = 2 # should load from config file

    def convert_trait_to_numerical_date(self, trait, dateFormat):
        for name, seq in self.seqs.iteritems():
            try:
                date_struc = parse_date(seq.attributes[trait], dateFormat)
                seq.attributes[trait] = date_struc[1]
            except KeyError:
                self.log.warn("Attribute {} not found for sequence {}. Ignoring".format(trait, seq.name))

    def codon_align(self):
        self.log.fatal("Codon align not yet implemented")

    def align(self, fname, debug=False):
        '''
        align sequences using mafft

        side-effects:
            self.aln {MultipleSeqAlignment} reference not present if not in self.seqs
            self.reference_aln {SeqRecord} always set, even if the reference is subsequently discarded
            self.sequence_lookup {dict} map linking seq.id to the alignment, potentialy without the reference
            saves the alignment (always including reference) to fname
        '''
        make_dir(self.run_dir)
        os.chdir(self.run_dir)
        if self.reference_in_dataset:
            out_seqs = self.seqs.values()
        else:
            self.log.notify("Adding reference for alignment step")
            out_seqs = self.seqs.values() + [self.reference_seq]

        SeqIO.write(out_seqs, "temp_in.fasta", "fasta")
        self.log.notify("Running alignment")
        os.system("mafft --anysymbol --thread " + str(self.nthreads) + " temp_in.fasta 1> temp_out.fasta 2>mafft_stderr")
        self.aln = AlignIO.read('temp_out.fasta', 'fasta')
        os.chdir("..")
        os.rename(os.path.join(self.run_dir, "temp_out.fasta"), fname)
        if not debug: remove_dir(self.run_dir)

        self.set_reference_alignment()
        if not self.reference_in_dataset:
            self.remove_reference_from_alignment()
        self.set_sequence_lookup()
        self.add_attributes_to_aln()

    def remove_reference_from_alignment(self):
        count = len(self.aln)
        self.aln = MultipleSeqAlignment([s for s in self.aln if s.name!=self.reference_seq.name])
        assert(count == (len(self.aln)+1))

    def set_reference_alignment(self):
        self.reference_aln = [x for x in list(self.aln) if x.name==self.reference_seq.name][0]

    def set_sequence_lookup(self):
        self.sequence_lookup = {seq.id:seq for seq in self.aln}

    def add_attributes_to_aln(self):
        for seqid, seq in self.seqs.iteritems():
            self.sequence_lookup[seqid].attributes = seq.attributes

    def try_restore_align_from_disk(self, fname):
        try:
            self.aln = AlignIO.read(fname, "fasta")
        except IOError:
            return
        except Exception as e:
            self.log.notify("Error restoring from alignment... re-doing")
            print(e)
            return

        try:
            self.set_reference_alignment()
        except IndexError:
            self.log.notify("Reference not found in alignment... re-doing")
            del self.aln
            return

        if not self.reference_in_dataset:
            self.remove_reference_from_alignment()

        if len({x.id for x in self.aln} ^ set(self.seqs.keys())) != 0:
            self.log.notify("Alignment on disk had different sequnces... re-doing")
            del self.aln
            del self.reference_aln
            return

        # at this stage we are happy with the alignment
        self.set_sequence_lookup()
        self.add_attributes_to_aln()
        self.log.notify("Alignment restored from disk")

    def strip_non_reference(self):
        ungapped = np.array(self.reference_aln)!='-'
        for seq in self.aln:
            seq.seq = Seq("".join(np.array(seq)[ungapped]))

    def remove_terminal_gaps(self):
        for seq in self.aln:
            seq_array = np.array(seq)
            seq_string = str(seq.seq)
            if (seq_array=='-').sum():
                left_gaps = len(seq_string) - len(seq_string.lstrip('-'))
                seq_array[:left_gaps] = 'N'
            if (seq_array=='-').sum():
                right_gaps = len(seq_string) - len(seq_string.rstrip('-'))
                if right_gaps:
                    seq_array[-right_gaps:] = 'N'
            seq.seq = Seq("".join(seq_array))

    def translate(self):
        '''
        make alignment of translations
        '''
        self.translations={}
        if not hasattr(self, "proteins"): # ensure dictionary to hold annotation
            self.proteins={}

        # add a default translation of the entire sequence unless otherwise specified
        if len(self.proteins)==0:
            self.proteins.update({'cds':FeatureLocation(start=0,
                end=self.aln.get_alignment_length(), strand=1)})

        for prot in self.proteins:
            aa_seqs = []
            for seq in self.aln:
                try:
                    # soon not needed as future biopython version will translate --- into -
                    tmpseq = self.proteins[prot].extract(seq)
                    tmpseq.attributes = seq.attributes
                    internal_gap = np.unique(np.where(np.array(tmpseq)=='-')[0]//3)
                    aa_seq = np.array(Seq(str(tmpseq.seq).replace('---', 'NNN')).translate())
                    aa_seq[internal_gap]='-'
                    tmpseq.seq = Seq("".join(aa_seq))
                except:
                    tmpseq.seq = Seq("".join([x if x in 'ACGT' else 'N'
                        for x in str(tmpseq.seq)])).translate()
                    print("Trouble translating",seq.id)
                aa_seqs.append(tmpseq)
            self.translations[prot] = MultipleSeqAlignment(aa_seqs)

    def clock_filter(self, root_seq=None, n_iqd=3, max_gaps = 1.0, plot=False):
        '''
        remove sequences form the set that are that evolve much faster or slower
        compared the majority. Regions with predominantly gaps can be removed since
        this can skew the evolutionary rates.
        '''
        if root_seq is None: # use consensus
            af = calc_af(self.aln, nuc_alpha)
            root_seq = np.fromstring(nuc_alpha, 'S1')[af.argmax(axis=0)]
        if type(root_seq)==str and root_seq in self.sequence_lookup:
            root_seq = np.array(self.sequence_lookup[root_seq])
        if max_gaps<1.0:
            af=calc_af(self.aln, nuc_alpha)
            good_pos = af[nuc_alpha.index('-')]<max_gaps
        else:
            good_pos = np.ones(self.aln.get_alignment_length(), dtype=bool)
        date_vs_distance = {}
        # self.reference_aln = None already set at alignment step
        for seq in self.aln:
            date_vs_distance[seq.id] = (seq.attributes['num_date'],
                np.mean((np.array(seq)!=root_seq)[(np.array(seq)!='-')&(root_seq!='-')&good_pos]))
            # if seq.id==self.reference.id:
            #     self.reference_aln = seq
        date_vs_distance_array=np.array(date_vs_distance.values())
        from scipy.stats import linregress, scoreatpercentile
        slope, intercept, rval, pval, stderr = linregress(date_vs_distance_array[:,0], date_vs_distance_array[:,1])
        print("distance vs time regression:",slope)
        residuals = (intercept + slope*date_vs_distance_array[:,0]) - date_vs_distance_array[:,1]
        IQD = scoreatpercentile(residuals, 75) - scoreatpercentile(residuals,25)
        if plot:
            import matplotlib.pyplot as plt
            plt.ion()
            plt.scatter(date_vs_distance_array[:,0], date_vs_distance_array[:,1], c='g')
            bad_points = abs(intercept+slope*date_vs_distance_array[:,0] - date_vs_distance_array[:,1])>n_iqd*IQD
            plt.scatter(date_vs_distance_array[bad_points,0], date_vs_distance_array[bad_points,1], c='r')


        print("before clock filter:",len(self.aln))
        tmp = {seq.id:seq for seq in self.aln
                if abs(intercept+slope*date_vs_distance[seq.id][0] - date_vs_distance[seq.id][1])<n_iqd*IQD}
        if self.reference.id not in tmp and self.reference.reference_in_dataset:
            self.log.notify('adding reference again after clock filter')
            tmp[self.reference.id] = self.reference_aln
        self.aln = MultipleSeqAlignment(tmp.values())
        print("after clock filter:",len(self.aln))

    def diversity_statistics(self):
        ''' calculate alignment entropy of nucleotide and optionally protein alignments '''
        if not hasattr(self, "aln"):
            self.log.fatal("Diversity statistics calculated before alignment generated.")
            return
        aln_array = np.array(self.aln)
        self.af = {'nuc': calc_af(self.aln, nuc_alpha)}
        tmp_af = self.af['nuc'][:-2]/self.af['nuc'][:-2].sum(axis=0)
        self.entropy ={'nuc': -(tmp_af*np.log(tmp_af+TINY)).sum(axis=0)}

        if hasattr(self, "translations"):
            for prot, aln in self.translations.iteritems():
                self.af[prot] = calc_af(aln, aa_alpha)
                tmp_af = self.af[prot][:-2]/self.af[prot][:-2].sum(axis=0)
                self.entropy[prot] = -(tmp_af*np.log(tmp_af+TINY)).sum(axis=0)

    def export_diversity(self, fname = 'entropy.json', indent=None):
        '''
        write the alignment entropy of each alignment (nucleotide and translations) to file
        '''
        if not hasattr(self, "entropy"):
            self.diversity_statistics()
        entropy_json = {}
        for feat in self.entropy:
            S = [max(0,round(x,4)) for x in self.entropy[feat]]
            n = len(S)
            if feat=='nuc':
                entropy_json[feat] = {'pos':range(0,n), 'codon':[x//3 for x in range(0,n)], 'val':S}
            else:
                entropy_json[feat] = {'pos':[x for x in self.proteins[feat]][::3],
                                      'codon':[(x-self.proteins[feat].start)//3 for x in self.proteins[feat]][::3], 'val':S}
        write_json(entropy_json, fname, indent=indent)
