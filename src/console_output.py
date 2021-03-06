from src.processing import Processing
from src.kMerAlignmentData import KMerAlignmentData
import math


# starts preprocess to calculate kmer-frequencies,etc and call print-methods
# data: file list
# k: kmer length
# peak: peak: peak-position, where sequences should be aligned
# top: number of best values
def printData(data, k, peak, top):
    feature = None
    cmd = True
    struct_data = None
    no_sec_peak = None
    process = Processing(data, data, k, peak, top, feature, cmd, struct_data, no_sec_peak)
    printPairwAlignment(process)
    printKMerFrequency(process)


# gets data and prints kmer-frequency table to stdout
# process: object, which contains information for further calculation-processes
def printKMerFrequency(process):
    char_space_ten = 10
    scaling_factor = 5
    top = process.getSettings().getTop()
    k = process.getSettings().getK()
    peak = process.getSettings().getPeak()
    selected = process.getSettings().getSelected()

    result = process.getTopKmer()
    freq_list = result['Frequency'].values.tolist()
    char_space = len(str(max(freq_list)))  # ascertains column space to maintain table readability
    tabs = 1
    if char_space >= char_space_ten:  # calculate tab count to maintain readability
        tabs = math.ceil(char_space / scaling_factor)

    file_list = result['File'].values.tolist()
    kmer_list = result.index.tolist()

    if top is None:
        top = len(process.getTopKmer())
        entry_count = top
    else:
        entry_count = len(kmer_list)
    print()
    print('Options:')
    print('k: {k}, peak: {p}, top: {t}, files: {f}'.
          format(k=k, p=peak, t=top, f=selected))
    print()
    print('k-Mer\t\tFrequency' + '\t' * tabs + 'File')
    for i in range(0, entry_count):
        print("{}\t\t{:<{space}}\t\t{}".format(kmer_list[i], freq_list[i], file_list[i], space=char_space))


# gets alignment data and prints alignment to stdout
# process: object, which contains information for further calculation-processes
def printPairwAlignment(process):
    try:
        alignment_lists, f1_name, f2_name = KMerAlignmentData.processData(process)

        if process.getSettings().getPeak() is None:
            print('Alignment of Top-kmere created with ClustalW')
            print('(for more information, see: http://www.clustal.org/clustal2/)')
            print("")
            name = f1_name
            for file in alignment_lists:
                print("File: " + name)
                for alg in file:
                    print(alg.seq)
                name = f2_name
                print()
        else:
            peak = process.getSettings().getPeak()
            k = process.getSettings().getK()
            print('Alignment of Top-{k}-mer created with Peak-Position: {p}'.format(k=k, p=peak))
            name = f1_name
            for file in alignment_lists:
                print("File: " + name)
                for alg in file:
                    print(alg)
                name = f2_name
                print()
    except ValueError:
        print("ERROR: Alignment cannot be calculated.")
