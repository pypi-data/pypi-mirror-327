from geolib.models.dstability.internal import *
from geolib.models.base_model_structure import BaseModelStructure
from geolib.geometry import Point
from typing import List, Optional


class PersistableSigmaTauTablePoint(DStabilitySubStructure):
    EffectiveStress: float = 0.0
    ShearStrength: float = 0.0


class PersistableSigmaTauTable(DStabilityBaseModelStructure):
    SigmaTauTablePoints: List[PersistableSigmaTauTablePoint] = []
    IsSigmaTauTableProbabilistic: bool = False
    SigmaTauTableVariationCoefficient: float = 0.0

    def to_global_sigma_tau_table(self):
        from geolib.soils import SigmaTauTablePoint

        sigma_tau_table = []
        for sigma_tau_table_point in self.SigmaTauTablePoints:
            sigma_tau_table.append(
                SigmaTauTablePoint(
                    shearStrength=sigma_tau_table_point.ShearStrength,
                    effective_stress=sigma_tau_table_point.EffectiveStress,
                )
            )
        return sigma_tau_table


class PersistableSoil:
    Code: str = ""
    Id: str = ""
    IsProbabilistic: bool = False
    Name: Optional[str] = ""
    Notes: Optional[str] = ""
    ShearStrengthModelTypeAbovePhreaticLevel: (
        ShearStrengthModelTypePhreaticLevelInternal
    ) = ShearStrengthModelTypePhreaticLevelInternal.MOHR_COULOMB_ADVANCED
    ShearStrengthModelTypeBelowPhreaticLevel: (
        ShearStrengthModelTypePhreaticLevelInternal
    ) = ShearStrengthModelTypePhreaticLevelInternal.SU
    MohrCoulombClassicShearStrengthModel: (
        PersistableMohrCoulombClassicShearStrengthModel
    ) = PersistableMohrCoulombClassicShearStrengthModel()
    MohrCoulombAdvancedShearStrengthModel: (
        PersistableMohrCoulombAdvancedShearStrengthModel
    ) = PersistableMohrCoulombAdvancedShearStrengthModel()
    SigmaTauTable: PersistableSigmaTauTable = PersistableSigmaTauTable()
    SuShearStrengthModel: PersistableSuShearStrengthModel = (
        PersistableSuShearStrengthModel()
    )
    VolumetricWeightAbovePhreaticLevel: float = 0.0
    VolumetricWeightBelowPhreaticLevel: float = 0.0
    SuTable: PersistableSuTable = PersistableSuTable()


############################################
# TEMP NEW CLASS TO ACCEPT 2024.02 version #
############################################
class DStabilityStructure(BaseModelStructure):
    """Highest level DStability class that should be parsed to and serialized from.

    The List[] items (one for each stage in the model) will be stored in a subfolder
    to multiple json files. Where the first (0) instance
    has no suffix, but the second one has (1 => _1) etc.

    also parses the outputs which are part of the json files
    """

    # input part
    waternets: List[Waternet] = [Waternet(Id="14")]  # waternets/waternet_x.json
    waternetcreatorsettings: List[WaternetCreatorSettings] = [
        WaternetCreatorSettings(Id="15")
    ]  # waternetcreatorsettings/waternetcreatorsettings_x.json
    states: List[State] = [State(Id="16")]  # states/states_x.json
    statecorrelations: List[StateCorrelation] = [
        StateCorrelation(Id="17")
    ]  # statecorrelations/statecorrelations_x.json
    scenarios: List[Scenario] = [
        Scenario(
            Id="0",
            Label="Scenario 1",
            Notes="Default Scenario by GEOLib",
            Stages=[
                Stage(
                    DecorationsId="12",
                    GeometryId="11",
                    Id="43",
                    Label="Stage 1",
                    LoadsId="18",
                    Notes="Default stage by GEOLib",
                    ReinforcementsId="19",
                    SoilLayersId="13",
                    StateId="16",
                    StateCorrelationsId="17",
                    WaternetCreatorSettingsId="15",
                    WaternetId="14",
                )
            ],
            Calculations=[
                PersistableCalculation(
                    CalculationSettingsId="20",
                    Id="42",
                    Label="Calculation 1",
                    Notes="Default calculation by GEOLib",
                )
            ],
        )
    ]
    soillayers: List[SoilLayerCollection] = [SoilLayerCollection(Id="13")]
    soilcorrelation: SoilCorrelation = SoilCorrelation()
    soils: SoilCollection = SoilCollection()
    soilvisualizations: SoilVisualisation = SoilVisualisation()
    reinforcements: List[Reinforcements] = [Reinforcements(Id="19")]
    projectinfo: ProjectInfo = ProjectInfo()
    nailproperties: NailProperties = NailProperties()
    loads: List[Loads] = [Loads(Id="18")]
    decorations: List[Decorations] = [Decorations(Id="12")]
    calculationsettings: List[CalculationSettings] = [CalculationSettings(Id="20")]
    geometries: List[Geometry] = [Geometry(Id="11")]

    # Output parts
    uplift_van_results: List[UpliftVanResult] = []
    uplift_van_particle_swarm_results: List[UpliftVanParticleSwarmResult] = []
    uplift_van_reliability_results: List[UpliftVanReliabilityResult] = []
    uplift_van_particle_swarm_reliability_results: List[
        UpliftVanParticleSwarmReliabilityResult
    ] = []
    spencer_results: List[SpencerResult] = []
    spencer_genetic_algorithm_results: List[SpencerGeneticAlgorithmResult] = []
    spencer_reliability_results: List[SpencerReliabilityResult] = []
    spencer_genetic_algorithm_reliability_results: List[
        SpencerGeneticAlgorithmReliabilityResult
    ] = []
    bishop_results: List[BishopResult] = []
    bishop_bruteforce_results: List[BishopBruteForceResult] = []
    bishop_reliability_results: List[BishopReliabilityResult] = []
    bishop_bruteforce_reliability_results: List[BishopBruteForceReliabilityResult] = []

    @model_validator(mode="after")
    def ensure_validity_foreign_keys(self):
        def list_has_id(values, id):
            for entry in values:
                if entry.Id == id:
                    return True
            return False

        for _, scenario in enumerate(self.scenarios):
            for _, stage in enumerate(scenario.Stages):
                if not list_has_id(self.decorations, stage.DecorationsId):
                    raise ValueError("DecorationsIds not linked!")
                if not list_has_id(self.geometries, stage.GeometryId):
                    raise ValueError("GeometryIds not linked!")
                if not list_has_id(self.loads, stage.LoadsId):
                    raise ValueError("LoadsIds not linked!")
                if not list_has_id(self.reinforcements, stage.ReinforcementsId):
                    raise ValueError("ReinforcementsIds not linked!")
                if not list_has_id(self.soillayers, stage.SoilLayersId):
                    raise ValueError("SoilLayersIds not linked!")
                if not list_has_id(self.states, stage.StateId):
                    raise ValueError("StateIds not linked!")
                if not list_has_id(self.statecorrelations, stage.StateCorrelationsId):
                    raise ValueError("StateCorrelationsIds not linked!")
                if not list_has_id(
                    self.waternetcreatorsettings, stage.WaternetCreatorSettingsId
                ):
                    raise ValueError("WaternetCreatorSettingsIds not linked!")
                if not list_has_id(self.waternets, stage.WaternetId):
                    raise ValueError("WaternetIds not linked!")
            for _, calculation in enumerate(scenario.Calculations):
                if not list_has_id(
                    self.calculationsettings, calculation.CalculationSettingsId
                ):
                    raise ValueError("CalculationSettingsIds not linked!")
        return self

    def add_default_scenario(
        self, label: str, notes: str, unique_start_id: Optional[int] = None
    ) -> Tuple[int, int]:
        """Add a new default (empty) scenario to DStability."""
        if unique_start_id is None:
            unique_start_id = self.get_unique_id()

        scenario_id = unique_start_id + 13

        self.waternets += [Waternet(Id=str(unique_start_id + 1))]
        self.waternetcreatorsettings += [
            WaternetCreatorSettings(Id=str(unique_start_id + 2))
        ]
        self.states += [State(Id=str(unique_start_id + 3))]
        self.statecorrelations += [StateCorrelation(Id=str(unique_start_id + 4))]
        self.soillayers += [SoilLayerCollection(Id=str(unique_start_id + 5))]
        self.soilcorrelation: SoilCorrelation = SoilCorrelation()
        self.reinforcements += [Reinforcements(Id=str(unique_start_id + 6))]
        self.loads += [Loads(Id=str(unique_start_id + 7))]
        self.decorations += [Decorations(Id=str(unique_start_id + 9))]
        self.calculationsettings += [CalculationSettings(Id=str(unique_start_id + 10))]
        self.geometries += [Geometry(Id=str(unique_start_id + 8))]
        self.scenarios += [
            Scenario(
                Id=str(scenario_id),
                Label=label,
                Notes=notes,
                Stages=[
                    Stage(
                        Id=str(unique_start_id + 11),
                        Label="Stage 1",
                        Notes="",
                        DecorationsId=str(unique_start_id + 9),
                        GeometryId=str(unique_start_id + 8),
                        LoadsId=str(unique_start_id + 7),
                        ReinforcementsId=str(unique_start_id + 6),
                        SoilLayersId=str(unique_start_id + 5),
                        StateId=str(unique_start_id + 3),
                        StateCorrelationsId=str(unique_start_id + 4),
                        WaternetCreatorSettingsId=str(unique_start_id + 2),
                        WaternetId=str(unique_start_id + 1),
                    )
                ],
                Calculations=[
                    PersistableCalculation(
                        Id=str(unique_start_id + 12),
                        Label="Calculation 1",
                        Notes="",
                        CalculationSettingsId=str(unique_start_id + 10),
                    )
                ],
            )
        ]

        return len(self.scenarios) - 1, scenario_id

    def add_default_stage(
        self,
        scenario_index: int,
        label: str,
        notes: str,
        unique_start_id: Optional[int] = None,
    ) -> Tuple[int, int]:
        """Add a new default (empty) stage to DStability."""
        if unique_start_id is None:
            unique_start_id = self.get_unique_id()

        stage_id = unique_start_id + 13

        self.waternets += [Waternet(Id=str(unique_start_id + 1))]
        self.waternetcreatorsettings += [
            WaternetCreatorSettings(Id=str(unique_start_id + 2))
        ]
        self.states += [State(Id=str(unique_start_id + 3))]
        self.statecorrelations += [StateCorrelation(Id=str(unique_start_id + 4))]
        self.soillayers += [SoilLayerCollection(Id=str(unique_start_id + 5))]
        self.soilcorrelation: SoilCorrelation = SoilCorrelation()
        self.reinforcements += [Reinforcements(Id=str(unique_start_id + 6))]
        self.loads += [Loads(Id=str(unique_start_id + 7))]
        self.decorations += [Decorations(Id=str(unique_start_id + 9))]
        self.geometries += [Geometry(Id=str(unique_start_id + 8))]

        new_stage = Stage(
            Id=str(stage_id),
            Label=label,
            Notes=notes,
            DecorationsId=str(unique_start_id + 9),
            GeometryId=str(unique_start_id + 8),
            LoadsId=str(unique_start_id + 7),
            ReinforcementsId=str(unique_start_id + 6),
            SoilLayersId=str(unique_start_id + 5),
            StateId=str(unique_start_id + 3),
            StateCorrelationsId=str(unique_start_id + 4),
            WaternetCreatorSettingsId=str(unique_start_id + 2),
            WaternetId=str(unique_start_id + 1),
        )

        scenario = self.scenarios[scenario_index]

        if scenario.Stages is None:
            scenario.Stages = []

        scenario.Stages.append(new_stage)
        return len(scenario.Stages) - 1, stage_id

    def add_default_calculation(
        self,
        scenario_index: int,
        label: str,
        notes: str,
        unique_start_id: Optional[int] = None,
    ) -> Tuple[int, int]:
        """Add a new default (empty) calculation to DStability."""
        if unique_start_id is None:
            unique_start_id = self.get_unique_id()

        calculation_id = unique_start_id + 13

        self.calculationsettings += [CalculationSettings(Id=str(unique_start_id + 1))]

        new_calculation = PersistableCalculation(
            Id=str(calculation_id),
            Label=label,
            Notes=notes,
            CalculationSettingsId=str(unique_start_id + 1),
        )

        scenario = self.scenarios[scenario_index]

        if scenario.Calculations is None:
            scenario.Calculations = []

        scenario.Calculations.append(new_calculation)
        return len(scenario.Calculations) - 1, calculation_id

    def get_unique_id(self) -> int:
        """Return unique id that can be used in DStability.
        Finds all existing ids, takes the max and does +1.
        """

        fk = ForeignKeys()
        classfields = fk.class_fields

        ids = []
        for instance in children(self):
            for field in classfields.get(instance.__class__.__name__, []):
                value = getattr(instance, field)
                if isinstance(value, (list, set, tuple)):
                    ids.extend(value)
                if isinstance(value, (int, float, str)):
                    ids.append(value)

        new_id = max({int(id) for id in ids if id is not None}) + 1
        return new_id

    def validator(self):
        return DStabilityValidator(self)

    def has_stage(self, scenario_index: int, stage_index: int) -> bool:
        try:
            scenario = self.scenarios[scenario_index]

            if scenario.Stages is None:
                return False

            scenario.Stages[stage_index]
            return True
        except IndexError:
            return False

    def has_calculation(self, scenario_index: int, calculation_index: int) -> bool:
        try:
            scenario = self.scenarios[scenario_index]

            if scenario.Calculations is None:
                return False

            scenario.Calculations[calculation_index]
            return True
        except IndexError:
            return False

    def has_scenario(self, scenario_index: int) -> bool:
        try:
            self.scenarios[scenario_index]
            return True
        except IndexError:
            return False

    def has_result(self, scenario_index: int, calculation_index: int) -> bool:
        if self.has_calculation(scenario_index, calculation_index):
            scenario = self.scenarios[scenario_index]

            if scenario.Calculations is None:
                return False

            result_id = scenario.Calculations[calculation_index].ResultId
            if result_id is None:
                return False
            else:
                return True
        return False

    def has_loads(self, scenario_index: int, stage_index: int) -> bool:
        if self.has_stage(scenario_index, stage_index):
            scenario = self.scenarios[scenario_index]

            if scenario.Stages is None:
                return False

            loads_id = scenario.Stages[stage_index].LoadsId
            if loads_id is None:
                return False
            else:
                return True
        return False

    def has_soil_layers(self, scenario_index: int, stage_index: int) -> bool:
        if self.has_stage(scenario_index, stage_index):
            scenario = self.scenarios[scenario_index]

            if scenario.Stages is None:
                return False

            soil_layers_id = scenario.Stages[stage_index].SoilLayersId
            if soil_layers_id is None:
                return False
            else:
                return True
        return False

    def has_soil_layer(
        self, scenario_index: int, stage_index: int, soil_layer_id: int
    ) -> bool:
        if self.has_soil_layers(scenario_index, stage_index):
            for layer in self.soillayers[stage_index].SoilLayers:
                if str(soil_layer_id) == layer.LayerId:
                    return True
            return False
        return False

    def has_reinforcements(self, scenario_index: int, stage_index: int) -> bool:
        if self.has_stage(scenario_index, stage_index):
            scenario = self.scenarios[scenario_index]

            if scenario.Stages is None:
                return False

            reinforcements_id = scenario.Stages[stage_index].ReinforcementsId
            if reinforcements_id is None:
                return False
            else:
                return True
        return False

    def _get_soil_layers(self, scenario_index: int, stage_index: int):
        soil_layers_id = self.scenarios[scenario_index].Stages[stage_index].SoilLayersId

        for soil_layers in self.soillayers:
            if soil_layers.Id == soil_layers_id:
                return soil_layers

        raise ValueError(
            f"No soil layers found for stage {stage_index} in scenario {scenario_index}."
        )

    def _get_excavations(self, scenario_index: int, stage_index: int):
        decorations_id = (
            self.scenarios[scenario_index].Stages[stage_index].DecorationsId
        )

        for decoration in self.decorations:
            if decoration.Id == decorations_id:
                return decoration.Excavations

        raise ValueError(
            f"No excavations found for stage {stage_index} in scenario {scenario_index}."
        )

    def _get_loads(self, scenario_index: int, stage_index: int):
        loads_id = self.scenarios[scenario_index].Stages[stage_index].LoadsId

        for loads in self.loads:
            if loads.Id == loads_id:
                return loads

        raise ValueError(
            f"No loads found for stage {stage_index} in scenario {scenario_index}."
        )

    def get_result_substructure(
        self, analysis_type: AnalysisTypeEnum, calculation_type: CalculationTypeEnum
    ) -> List[DStabilityResult]:
        result_types_mapping = {
            AnalysisTypeEnum.UPLIFT_VAN: {
                "non_probabilistic": self.uplift_van_results,
                "probabilistic": self.uplift_van_reliability_results,
            },
            AnalysisTypeEnum.UPLIFT_VAN_PARTICLE_SWARM: {
                "non_probabilistic": self.uplift_van_particle_swarm_results,
                "probabilistic": self.uplift_van_particle_swarm_reliability_results,
            },
            AnalysisTypeEnum.SPENCER_GENETIC: {
                "non_probabilistic": self.spencer_genetic_algorithm_results,
                "probabilistic": self.spencer_genetic_algorithm_reliability_results,
            },
            AnalysisTypeEnum.SPENCER: {
                "non_probabilistic": self.spencer_results,
                "probabilistic": self.spencer_reliability_results,
            },
            AnalysisTypeEnum.BISHOP_BRUTE_FORCE: {
                "non_probabilistic": self.bishop_bruteforce_results,
                "probabilistic": self.bishop_bruteforce_reliability_results,
            },
            AnalysisTypeEnum.BISHOP: {
                "non_probabilistic": self.bishop_results,
                "probabilistic": self.bishop_reliability_results,
            },
        }

        if calculation_type == CalculationTypeEnum.PROBABILISTIC:
            return result_types_mapping[analysis_type]["probabilistic"]

        return result_types_mapping[analysis_type]["non_probabilistic"]


class Waternet(Waternet):
    def add_reference_line(
        self,
        reference_line_id: str,
        label: str,
        notes: str,
        points: List[Point],
        bottom_head_line_id: Optional[str] = None,
        top_head_line_id: Optional[str] = None,
    ) -> PersistableReferenceLine:
        reference_line = PersistableReferenceLine(
            Id=reference_line_id, Label=label, Notes=notes
        )
        reference_line.Points = [PersistablePoint(X=p.x, Z=p.z) for p in points]

        if bottom_head_line_id is not None and not self.has_head_line_id(
            bottom_head_line_id
        ):
            raise ValueError(
                f"Unknown headline id {bottom_head_line_id} for bottom_head_line_id"
            )

        if top_head_line_id is not None and not self.has_head_line_id(top_head_line_id):
            raise ValueError(
                f"Unknown headline id {top_head_line_id} for top_head_line_id"
            )

        reference_line.BottomHeadLineId = bottom_head_line_id
        reference_line.TopHeadLineId = top_head_line_id

        self.ReferenceLines.append(reference_line)
        return reference_line
