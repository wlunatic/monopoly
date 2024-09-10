from monopoly.banks import BankDetector, banks
from monopoly.generic import GenericBank
from monopoly.pdf import PdfDocument, PdfParser
from monopoly.pipeline import Pipeline
import argparse
import pathlib

def main():
    # Initialize parser
    parser = argparse.ArgumentParser()

    # Adding optional argument
    parser.add_argument("-f", "--file", help = "Define the single input directory (Must be PDF)")
    parser.add_argument("-d", "--directory", help = "Define Input directory (used for parsing all files in directory)")
    parser.add_argument("-o", "--output", help = "Define Output directory")

    # Read arguments from command line
    args = parser.parse_args()

    if not args.file and not args.directory:
        raise RuntimeError("Please define `--file` or `--directory` for your input")
    
    if not args.output:
        raise RuntimeError("Please define `--output` for your output directory")
    
    input_dir = args.directory if not args.file else args.file
    output_dir = args.output
    
    example(input_dir, output_dir)
    
def runPipeline(filename, output):
    
    document = PdfDocument(file_path=filename)
    analyzer = BankDetector(document)
    bank = analyzer.detect_bank(banks) or GenericBank
    parser = PdfParser(bank, document)
    pipeline = Pipeline(parser)

    # This runs pdftotext on the PDF and
    # extracts transactions as raw text
    statement = pipeline.extract()

    # Dates are converted into an ISO 8601 date format
    transactions = pipeline.transform(statement)
    
    # Parsed transactions writen to a CSV file in the "example" directory
    pipeline.load(
        transactions=transactions,
        statement=statement,
        output_directory=output,
    )
    

def example(input_dir: str, output_dir: str):
    """Example showing how monopoly can be used to extract data from
    a single bank statement

    You can pass in the bank class if you want to specify a specific bank,
    or ignore the bank argument and let the Pipeline try to automatically
    detect the bank.
    """
    
    if (input_dir.endswith(".pdf")):
        runPipeline(input_dir, output_dir)
    else:
        for pdf_file in pathlib.Path(input_dir).glob('*.pdf'):
            runPipeline(pdf_file, output_dir)
    
if __name__ == "__main__":
    main()
