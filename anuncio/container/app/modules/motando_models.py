#
# modules/motando_models.py
#

from typing import Optional, List
from pydantic import BaseModel, Field, PositiveInt, constr


class AnuncioModel(BaseModel):
    moto_marca: PositiveInt = Field(..., gt=0)
    moto_modelo: PositiveInt = Field(..., gt=0)
    ano_fabricacao: str = Field(..., max_length=4, min_length=4)
    ano_modelo: str = Field(..., max_length=4, min_length=4)
    placa: str = Field(..., max_length=20)
    km: int
    zero_km: bool = False
    cor: str
    preco: float
    frase_vendedora: str = Field(..., max_length=500)
    descricao: Optional[constr(max_length=2000)]
    opcional_alarme: bool = False
    opcional_bau: bool = False
    opcional_computador: bool = False
    opcional_gps: bool = False
    aceita_contraoferta: bool = False
    aceita_troca: bool = False
    doc_ok: bool = Field(..., exclude=True)
    sinistro: bool = Field(..., exclude=True)
    trilha_pista: bool = Field(..., exclude=True)
    freios: Optional[str]
    tipo_partida: Optional[str]
    refrigeracao: Optional[str]
    estilo: Optional[str]
    origem: Optional[str]
    upload_img_lista: List[str]


class AnuncioModelDb(BaseModel):
    pass