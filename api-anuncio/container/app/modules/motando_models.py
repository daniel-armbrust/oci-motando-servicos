#
# modules/motando_models.py
#

from datetime import datetime

from typing import Optional, List
from pydantic import BaseModel, Field, constr, EmailStr


class AnuncioBase(BaseModel):
    moto_marca: int = Field(..., gt=0)
    moto_modelo: int = Field(..., gt=0)
    ano_fabricacao: int = Field(..., gt=1000)
    ano_modelo: int = Field(..., gt=1000)
    placa: str = Field(..., max_length=20)
    km: int = Field(..., ge=0)
    zero_km: bool = False
    cor: str = 'Não especificado'
    preco: float
    frase_vendedora: Optional[constr(max_length=500)]
    descricao: Optional[constr(max_length=2000)]
    opcional_alarme: bool = False
    opcional_bau: bool = False
    opcional_computador: bool = False
    opcional_gps: bool = False
    aceita_contraoferta: Optional[bool]
    aceita_troca: Optional[bool]
    doc_ok: Optional[bool]
    sinistro: Optional[bool]
    trilha_pista: Optional[bool]
    freios: str = 'Não especificado'
    tipo_partida: str = 'Não especificado'
    refrigeracao: str = 'Não especificado'
    estilo: str = 'Não especificado'
    origem: str = 'Não especificado'
    img_lista: List[str]


class AnuncioModel(AnuncioBase):
    pass


class AnuncioModelDb(AnuncioBase):
    __ts_now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

    email: EmailStr       
    data_cadastro: str = __ts_now
    data_modificacao: str = __ts_now