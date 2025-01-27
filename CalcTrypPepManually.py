import re

def read_fasta(file_path):
    """Reads a FASTA file and returns a dictionary with specific accession numbers and sequences as values."""
    sequences = {}
    with open(file_path, 'r') as file:
        accession = None
        sequence = []
        for line in file:
            line = line.strip()
            if line.startswith(">"):
                if accession:
                    sequences[accession] = ''.join(sequence)
                header_parts = line.split('|')
                if len(header_parts) > 1:
                    accession = header_parts[1]  # Extract the part between the pipe signs
                else:
                    accession = line.split()[0][1:]  # Fallback to simple accession extraction
                sequence = []
            else:
                sequence.append(line)
        if accession:
            sequences[accession] = ''.join(sequence)
    return sequences

def read_accessions_from_txt(txt_file_path):
    """Reads a text file and returns a list of accession numbers."""
    with open(txt_file_path, 'r') as file:
        accessions = [line.strip() for line in file if line.strip()]
    return accessions

def trypsin_digest(sequence):
    """Returns the number of peptides after trypsin digestion with lengths between 7 and 50."""
    pattern = re.compile(r"(?<=[KR])(?!P)")
    peptides = pattern.split(sequence)
    filtered_peptides = [peptide for peptide in peptides if 7 <= len(peptide) <= 50]
    return len(filtered_peptides)

def count_trypsin_peptides_for_accessions(fasta_file_path, txt_file_path):
    """Counts the number of peptides resulting from trypsin digestion for each sequence with accession numbers from the text file."""
    sequences = read_fasta(fasta_file_path)
    accessions = read_accessions_from_txt(txt_file_path)

    results = []
    for accession in accessions:
        if accession in sequences:
            sequence = sequences[accession]
            num_peptides = trypsin_digest(sequence)
            results.append((accession, num_peptides))
        else:
            results.append((accession, None))  # Accession not found in the FASTA file
    return results

def write_results_to_txt(results, output_file_path):
    """Writes the results to a text file."""
    with open(output_file_path, 'w') as file:
        for accession, num_peptides in results:
            if num_peptides is not None:
                file.write(f"{accession}, {num_peptides}\n")
            else:
                file.write(f"{accession} not found in the FASTA file\n")

# Example usage:

##Humans
fasta_file = '/home/melissa/Downloads/RefSeq/ViaFragpipe/Human/2023-06-01-decoys-isoforms-contam-UP000005640.fas'
txt_file = '/home/melissa/Downloads/RefSeq/ViaFragpipe/Human/Human_TBI_ProteinHitListAccessions'
output_file = '/home/melissa/Downloads/RefSeq/ViaFragpipe/Human/HumanTotalTryptic_output1.txt'
'''
#Mouse
fasta_file = '/home/melissa/Downloads/RefSeq/ViaFragpipe/Mouse/2023-06-01-decoys-isoforms-contam-UP000000589.fas'
txt_file = '/home/melissa/Downloads/RefSeq/ViaFragpipe/Mouse/Mouse_TBI_ProteinHitListAccessions'
output_file = '/home/melissa/Downloads/RefSeq/ViaFragpipe/Mouse/MouseTotalTryptic_output.txt'
'''
'''
#Rat
fasta_file = '/home/melissa/Downloads/RefSeq/ViaFragpipe/Rat/2023-06-01-decoys-isoforms-contam-UP000002494.fas'
txt_file = '/home/melissa/Downloads/RefSeq/ViaFragpipe/Rat/Rat_TBI_ProteinHitListAccessions'
output_file = '/home/melissa/Downloads/RefSeq/ViaFragpipe/Rat/RatTotalTryptic_output.txt'
'''

'''
#Droso
fasta_file = '/home/melissa/Downloads/RefSeq/ViaFragpipe/FruitFly/2023-06-01-decoys-isoforms-contam-UP000000803.fas'
txt_file = '/home/melissa/Downloads/RefSeq/ViaFragpipe/FruitFly/Droso_TBI_ProteinHitListAccessions'
output_file = '/home/melissa/Downloads/RefSeq/ViaFragpipe/FruitFly/DrosoTotalTryptic_output.txt'
'''

try:
    results = count_trypsin_peptides_for_accessions(fasta_file, txt_file)
    write_results_to_txt(results, output_file)
except Exception as e:
    print(e)
