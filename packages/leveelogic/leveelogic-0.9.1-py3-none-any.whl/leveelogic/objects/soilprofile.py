from typing import List, Optional, Tuple
import math
import pandas as pd

from ..models.datamodel import DataModel
from .soillayer import SoilLayer
from .soilpolygon import SoilPolygon
from .soilcollection import SoilCollection
from ..settings import UNIT_WEIGHT_WATER
from .stresses import Stresses


class SoilProfile(DataModel):
    soillayers: List[SoilLayer] = []

    @property
    def top(self):
        return self.soillayers[0].top

    @property
    def bottom(self):
        return self.soillayers[-1].bottom

    def soillayer_at_z(self, z: float) -> Optional[SoilLayer]:
        """Get the soillayer at the given z coordinate

        Args:
            z (float): z coordinate

        Returns:
            Optional[SoilLayer]: The soillayer at the given depth or None if no soillayer is found
        """
        for sl in self.soillayers:
            if z <= sl.top and z >= sl.bottom:
                return sl

        return None

    def merge(self):
        """Merge the soillayers if two or more consecutive soillayers are of the same type"""
        result = []
        for i in range(len(self.soillayers)):
            if i == 0:
                result.append(self.soillayers[i])
            else:
                if self.soillayers[i].soilcode == result[-1].soilcode:
                    result[-1].bottom = self.soillayers[i].bottom
                else:
                    result.append(self.soillayers[i])
        self.soillayers = result

    def to_soilpolygons(self, left: float, right: float) -> List[SoilPolygon]:
        result = []
        for layer in self.soillayers:
            result.append(
                SoilPolygon(
                    points=[
                        (left, layer.top),
                        (right, layer.top),
                        (right, layer.bottom),
                        (left, layer.bottom),
                    ],
                    soilcode=layer.soilcode,
                )
            )
        return result

    def set_top(self, top: float):
        self.soillayers[0].top = top

    def set_bottom(self, bottom: float):
        self.soillayers[-1].bottom = bottom

    def stresses(
        self,
        soil_collection: SoilCollection,
        phreatic_level: float,
        load: float = 0.0,
    ) -> Stresses:  # z, s_tot, u, s_eff
        result = Stresses()

        s_tot = load
        u = 0.0

        if self.top < phreatic_level:
            result.add(z=phreatic_level, s_tot=s_tot, u=0.0)
            u += (phreatic_level - self.top) * UNIT_WEIGHT_WATER

        result.add(z=self.top, s_tot=s_tot + u, u=u)

        for layer in self.soillayers:
            soil = soil_collection.get(layer.soilcode)
            if layer.top <= phreatic_level:
                u += layer.height * UNIT_WEIGHT_WATER
                s_tot += layer.height * soil.ys
                result.add(z=layer.bottom, s_tot=s_tot, u=u)
            elif layer.bottom >= phreatic_level:
                s_tot += layer.height * soil.yd
                result.add(z=layer.bottom, s_tot=s_tot, u=0.0)
            else:
                s_tot += (layer.top - phreatic_level) * soil.yd
                result.add(z=phreatic_level, s_tot=s_tot, u=0.0)
                s_tot += (phreatic_level - layer.bottom) * soil.ys
                u += (phreatic_level - layer.bottom) * UNIT_WEIGHT_WATER
                result.add(z=layer.bottom, s_tot=s_tot, u=u)

        return result

    def u_settlement(
        self,
        phreatic_level: float,
        waterloads: List[Tuple[float, float]],
        soil_collection: SoilCollection,
    ):
        # calculate initial stresses
        # s_ini = self.stresses(
        #     soil_collection=soil_collection,
        #     phreatic_level=phreatic_level,
        # )

        cv_dict = {s.code: s.cv for s in soil_collection.soils}
        yd_dict = {s.code: s.yd for s in soil_collection.soils}
        ys_dict = {s.code: s.ys for s in soil_collection.soils}

        # bundle cohesive layers
        layers = [[0, sl] for sl in self.soillayers]  # cv group, soillayer
        icv, last_used_icv = 1, 0
        for i, sl in enumerate(self.soillayers):
            soil = soil_collection.get(soilcode=sl.soilcode)
            if soil.cv >= 1e-3:  # drained
                layers[i] = [0, layers[i][1]]
                icv = max([l[0] for l in layers]) + 1
            else:
                layers[i] = [icv, layers[i][1]]

        d = {
            "soilcode": [sl.soilcode for sl in self.soillayers],
            "top": [sl.top for sl in self.soillayers],
            "bottom": [sl.bottom for sl in self.soillayers],
            "height": [sl.height for sl in self.soillayers],
            "yd": [yd_dict[sl.soilcode] for sl in self.soillayers],
            "ys": [ys_dict[sl.soilcode] for sl in self.soillayers],
            "cv": [cv_dict[sl.soilcode] for sl in self.soillayers],
            "cv_group": [l[0] for l in layers],
            "cv_eq": [0] * len(layers),
        }

        df = pd.DataFrame(d)

        for i in range(0, icv):
            if i == 0:
                df[df["cv_group"] == 0].cv_eq = df.cv
        i = 1

    def settlement(
        self,
        load: Optional[float] = None,
        spread: Optional[float] = None,
        phreatic_level: Optional[float] = None,
        new_phreatic_level: Optional[float] = None,
    ) -> List[Tuple[float, float]]:
        pass
