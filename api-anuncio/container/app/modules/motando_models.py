#
# modules/motando_models.py
#

from datetime import datetime

from typing import Optional, List, Union
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
    moto_marca: Union[str, int]    
    moto_modelo: Union[str, int]   
    img_lista: List[dict] 
    publicado: bool = False  
    vendido: bool = False  
    data_cadastro: str = __ts_now
    data_modificacao: str = __ts_now


class AnuncioModelDbOut(BaseModel):
    id: int = Field(..., gt=0)
    moto_marca: str
    moto_modelo: str
    ano_fabricacao: int = Field(..., gt=1000)
    ano_modelo: int = Field(..., gt=1000)
    placa: str = Field(..., max_length=20)
    km: int = Field(..., ge=0)
    zero_km: bool
    cor: str
    preco: float
    frase_vendedora: str
    descricao: str
    opcional_alarme: bool
    opcional_bau: bool
    opcional_computador: bool
    opcional_gps: bool
    aceita_contraoferta: Optional[bool]
    aceita_troca: Optional[bool]
    doc_ok: Optional[bool]
    sinistro: Optional[bool]
    trilha_pista: Optional[bool]
    freios: str
    tipo_partida: str
    refrigeracao: str
    estilo: str 
    origem: str 
    img_lista: List[str]
    

class AnuncioModelList(BaseModel):
   id: int
   moto_marca: str
   moto_modelo: str
   ano_fabricacao: str
   ano_modelo: str
   km: int = Field(..., ge=0)
   zero_km: bool
   cor: str
   preco: float
   data_cadastro: str
   status: str 
   vendido: bool
   img_lista: Optional[List[str]]