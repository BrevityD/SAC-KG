import argparse
import json
from pathlib import Path
from typing import Dict

from dotenv import load_dotenv
from loguru import logger

from corpus import SeeridiaChemistryNoteCorpus
from frame import Entities, Reactions
from model_response import ModelResponse
from prompt import load_prompts

class Pipeline:
    def __init__(self):
        self.prompts = load_prompts()
        self.model = ModelResponse()

    def extract_entities(self, text_file: str) -> Dict:
        prompt = self.prompts["ExtractEntitiesPrompt"]
        system_prompt = prompt["system"]

        with open(text_file, "r", encoding="utf8") as f:
            text = "\n".join(f.readlines())
        corpus = SeeridiaChemistryNoteCorpus(text)
        corpus.clean()
        logger.debug("Corpus processed")
        user_prompt = self.model.render_prompt(prompt, domain_text=corpus.get_samples(0))

        response = self.model.call_model(
            system_prompt,
            user_prompt,
            model="gpt-4o-mini",
            out_structure=Entities
        )
        return json.loads(response.model_dump_json())

    def extract_reactions(self, text_file: str) -> Dict:
        prompt = self.prompts["ExtractReactionsPrompt"]
        system_prompt = prompt["system"]
        example = self.prompts["ExtractReactionExample"]["prompt"]

        with open(text_file, "r", encoding="utf8") as f:
            text = "\n".join(f.readlines())
        corpus = SeeridiaChemistryNoteCorpus(text)
        corpus.clean()
        logger.debug("Corpus processed")
        user_prompt = self.model.render_prompt(
            prompt,
            domain_text=corpus.get_samples(0),
            example=example
        )

        response = self.model.call_model(
            system_prompt,
            user_prompt,
            out_structure=Reactions
        )
        return json.loads(response.model_dump_json())

def main():
    parser = argparse.ArgumentParser(description="Chemical Information Extraction Pipeline")
    parser.add_argument("--text", type=str, required=True, help="Input text file to process")
    parser.add_argument("--mode", type=str, required=True, 
                        choices=["entities", "reactions"], 
                        help="Extraction mode: entities or reactions")
    parser.add_argument("--output_file", type=str, required=True, help="Output file name")

    args = parser.parse_args()
    load_dotenv()
    pipeline = Pipeline()

    logger.debug(f"You are trying to extract {args.mode} in {args.text} and save to {args.output_file}")

    if args.mode == "entities":
        result = pipeline.extract_entities(args.text)
    else:
        result = pipeline.extract_reactions(args.text)

    with open(Path("output", args.output_file), "w", encoding="utf8") as f:
        json.dump(result, f, indent=4)

    logger.debug(f"Final Result:\n{result}")

if __name__ == "__main__":
    main()
