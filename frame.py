from enum import Enum
from typing import List, Optional, Union
from pydantic import BaseModel

class CompoundType(Enum):
    SIMPLESUBSTANCE = "SimpleSubstance"
    OXIDE = "Oxide"
    ACID = "Acid"
    ALKALI = "Alkali"
    SALT = "Salt"

class CompoundProperty(Enum):
    OXIDATION = "Oxidation"
    REDUCTIVENESS = "Reductiveness"
    OTHERS = "Others"

class ReactionType(Enum):
    REDOX = "Redox"
    NEUTRALIZATION = "Neutralization"
    OTHERS = "Others"

class EntityType(Enum):
    ELEMENT = "Element"
    COMPOUND = "Compound"
    ION = "Ion"

class StateOfMatter(Enum):
    SOLID = "Solid"
    LIQUID = "Liquid"
    GAS = "Gas"
    OTHERS = "Others"

class Entity(BaseModel):
    entity_type: EntityType
    entity_name: str

class Entities(BaseModel):
    entities: List[Entity]

class PhysicalProperties(BaseModel):
    color: Union[str, None]
    state_of_matter: Union[StateOfMatter, None]
    molecule_weight: Union[float, None]
    melting_point: Union[float, None]
    boiling_point: Union[float, None]
    density: Union[float, None]

class Element(BaseModel):
    element_name: str
    element_symbol: str
    atomic_number: Union[int, None]
    atomic_weight: Union[float, None]
    electron_configuration: Union[str, None]
    simple_substance_property: PhysicalProperties

class Compound(BaseModel):
    compound_name: Union[str, None]
    compound_formula: Union[str, None]
    compound_elements: List[Element]
    compound_type: CompoundType
    physical_properties: PhysicalProperties
    chem_properties: Union[List[CompoundProperty], None]

class Ion(BaseModel):
    ion_name: str
    ion_formula: str
    electric_charges: str

class Reaction(BaseModel):
    reaction_type: ReactionType
    equation: str
    conditions: Optional[str]
    reactants: List[str]
    products: List[str]
    # reactants: List[Union[Compound, Ion]]
    # products: List[Union[Compound, Ion]]

class Reactions(BaseModel):
    reactions: List[Reaction]
