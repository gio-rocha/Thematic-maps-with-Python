# Thematic-maps-with-Python

# Overview

This repository contains thematic maps developed in Python for cartographic representation of environmental and territorial variables at different spatial scales. The maps are designed to support geographic visualization and interpretation of spatial patterns related to physical and environmental characteristics.

# Objectives
- Create thematic maps for geographic and environmental applications.
- Represent spatial distribution of environmental classes and categories
- Improve visual interpretation of territorial data
- Apply Python tools for thematic cartographic production
  
# Data
  - *Brazilian Territorial Mesh (Federal Units)*
    - Source: IBGE – Instituto Brasileiro de Geografia e Estatística  
    - Description: Official cartographic boundaries of Brazilian states (Unidades da Federação)
    - 🔗 [Download Data](https://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/municipio_2025/Brasil/BR_UF_2025.zip)


  - *Municipal Boundaries – Rio de Janeiro State*
    - Source: IBGE – Instituto Brasileiro de Geografia e Estatística  
    - Description: Municipal-level territorial divisions for the state of Rio de Janeiro
    - 🔗 [Download Data](https://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/municipio_2025/UFs/RJ/RJ_Municipios_2025.zip)


  - *Brazilian Major Regions (Grandes Regiões)*
    - Source: IBGE – Instituto Brasileiro de Geografia e Estatística  
    - Description: Official regional division of Brazil into five major regions (North, Northeast, Central-West, Southeast, and South)
    - 🔗 [Download Data](https://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/municipio_2025/Brasil/BR_Regioes_2025.zip)


  - *Brazilian Biomes Boundaries*
    - Source: IBGE – Instituto Brasileiro de Geografia e Estatística  
    - Description: Official spatial boundaries of Brazilian biomes, including the Amazon, Cerrado, Atlantic Forest, Caatinga, Pantanal, and Pampa, used for environmental and geographic analysis.  
    - 🔗 [Download Data](https://www.ibge.gov.br/geociencias/informacoes-ambientais/vegetacao/15842-biomas.html?=&t=downloads) (*Biomas_250mil.zip*)

   
  - *Soil Classification (Brazil)*
    - Source: IBGE – Instituto Brasileiro de Geografia e Estatística  
    - Description: Spatial dataset representing soil classes across Brazil, used for environmental analysis, land use studies, and thematic mapping  
    - 🔗 [Download Data](https://www.ibge.gov.br/geociencias/informacoes-ambientais/pedologia/10871-pedologia.html?=&t=downloads) (*PD_ORDEM.zip*)


  - *States-level Greenhouse Gas Emissions Data*
    - Source: SEEG - Sistema de Estimativas de Emissões e Remoções de Gases de Efeito Estufa
    - Description: Annual greenhouse gas emissions data aggregated at the state level across Brazil, covering multiple sectors and gases
    - 🔗 [Download Data](https://seeg.eco.br/wp-content/uploads/2025/12/Dados-nacionais-13.0.xlsx)


  - *Municipality-level Greenhouse Gas Emissions Data*
    - Source: SEEG - Sistema de Estimativas de Emissões e Remoções de Gases de Efeito Estufa
    - Description: Greenhouse gas emissions data disaggregated at the municipal level, enabling detailed local-scale analysis across Brazil 
    - 🔗 [Download Data](https://drive.google.com/drive/folders/1UQ9vRnemajFFbezdyTxJXhxUGsavm7-F?usp=sharing)


# Tools and Libraries
- Python
- Matplotlib
- GeoPandas
- Cartopy

# Outputs
- Thematic map of Brazilian biomes
  <img width="4500" height="4350" alt="Biomas_Br" src="https://github.com/user-attachments/assets/e8c6f1b2-02ec-4997-b5b0-e0bffc375f24" />

- Thematic map of soil types in Minas Gerais
  <img width="4880" height="3400" alt="Solos-Mapa-MG" src="https://github.com/user-attachments/assets/e44a2ff5-542f-4e99-9cf4-624c5475b4b0" />
  
- Thematic figure of greenhouse gas emissions by sector in São Paulo and Mato Grosso
  <img width="4280" height="2679" alt="GEEs_SP_MT" src="https://github.com/user-attachments/assets/6bd65f0c-98b4-43e6-86bf-d86115fd94ab" />

- Thematic figure showing the temporal evolution of greenhouse gas emissions in Guapimirim
  <img width="5360" height="3479" alt="Mapa_GEEs_Guapi" src="https://github.com/user-attachments/assets/e3c99b1b-dff5-48d6-8877-f1e54de52f8c" />
