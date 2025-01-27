def count_peptides_within_criteria(digested_peptides, accessions):
    """Count the peptides that meet the criteria and group them by accession number."""
    peptide_counts = {accession: 0 for accession in accessions}

    for peptide in digested_peptides:
        accession = peptide['protein']
        if accession in accessions:
            length = len(peptide['sequence'])
            mass = peptide['mass']
            if 7 <= length <= 50 and 500 <= mass <= 5000:
                peptide_counts[accession] += 1
    print(peptide_counts)
    return peptide_counts


def test_count_peptides_within_criteria():
    sample_digested_peptides = [
        {'sequence': 'ABCDEK', 'protein': 'P12345', 'mass': 100},
        {'sequence': 'FGHIKLMN', 'protein': 'P12345', 'mass': 800},
        {'sequence': 'PQRST', 'protein': 'P67890', 'mass': 450},
        {'sequence': 'VWXY', 'protein': 'P67890', 'mass': 300},
        {'sequence': 'ABCDEKFGHIKLMNPQRSTVWXY', 'protein': 'P11111', 'mass': 5500},
        {'sequence': 'STUVWXYZ', 'protein': 'P12345', 'mass': 1100},
        {'sequence': 'ABCDEFGHIJK', 'protein': 'P67890', 'mass': 1000}
    ]

    sample_accessions = ['P12345', 'P67890', 'P11111']

    expected_output = {
        'P12345': 2,  # Only 'FGHIKLMN' and 'STUVWXYZ' meet the criteria
        'P67890': 1,  # Only 'ABCDEFGHIJK' meets the criteria
        'P11111': 0  # No peptides meet the criteria
    }

    output = count_peptides_within_criteria(sample_digested_peptides, sample_accessions)

    assert output == expected_output, f"Expected {expected_output}, but got {output}"
    print("All test cases passed!")


# Run the test function
test_count_peptides_within_criteria()

import csv

def parse_chainsaw_output(output_file):
    """Parse the output from the Chainsaw command-line tool."""
    digested_peptides = []
    with open(output_file, 'r', newline='') as file:
        reader = csv.DictReader(file, delimiter='\t')
        for row in reader:
            accession = row['protein'].split('|')[1]  # Extract accession between pipe symbols
            peptide = {
                'sequence': row['sequence'],
                'protein': accession,
                'mass': float(row['mass'])  # Convert mass to float
                # Add more fields if needed
            }
            digested_peptides.append(peptide)
    return digested_peptides

def read_accessions_from_txt(txt_file_path):
    """Reads a text file and returns a list of accession numbers."""
    with open(txt_file_path, 'r') as file:
        accessions = [line.strip() for line in file if line.strip()]
    return accessions

def count_peptides_within_criteria(digested_peptides, accessions):
    """Count the peptides that meet the criteria and save them grouped by accession number."""
    peptide_counts = {accession: {'count': 0, 'peptides': []} for accession in accessions}

    for peptide in digested_peptides:
        accession = peptide['protein']
        if accession in accessions:
            length = len(peptide['sequence'])
            mass = peptide['mass']
            if 7 <= length <= 50 and 500 <= mass <= 5000:
                peptide_counts[accession]['count'] += 1
                peptide_counts[accession]['peptides'].append(peptide['sequence'])

    print(peptide_counts)
    return peptide_counts

def write_grouped_peptides_to_txt(peptide_counts, output_file_path):
    """Writes the peptide counts and sequences to a text file."""
    with open(output_file_path, 'w') as file:
        for accession, data in peptide_counts.items():
            file.write(f"{accession}: {data['count']} peptides\n")
            for peptide in data['peptides']:
                file.write(f"  {peptide}\n")

# Example usage:

# Define file paths


chainsaw_output_file = '/home/melissa/Downloads/RefSeq/ViaFragpipe/Human/2023-06-01-decoys-isoforms-contam-UP000005640.fas_digestedPeptides.tsv'  # Replace with the path to the Chainsaw output TSV file
accessions_txt_file = '/home/melissa/Downloads/RefSeq/ViaFragpipe/Human/Human_TBI_ProteinHitListAccessions'  # Replace with the path to the accession numbers text file
output_file = '/home/melissa/Downloads/RefSeq/ViaFragpipe/Human/HumanMaxTryptic_peptides_count3.txt'  # Replace with the desired output file path
# Parse the Chainsaw output and read the accessions
try:
    digested_peptides = parse_chainsaw_output(chainsaw_output_file)
    accessions = read_accessions_from_txt(accessions_txt_file)

    # Group the peptides within criteria and count them
    peptide_counts = count_peptides_within_criteria(digested_peptides, accessions)

    # Write the results to a text file
    write_grouped_peptides_to_txt(peptide_counts, output_file)
except Exception as e:
    print(e)
