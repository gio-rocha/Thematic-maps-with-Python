#SCRIPT PARA EMISSÃO DE GEEs ao longo do tempo para uma cidade

######### IMPORTANDO BIBLIOTECAS ###########
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib_scalebar.scalebar import ScaleBar
from matplotlib.patches import Rectangle
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
from matplotlib.ticker import FuncFormatter
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.io.shapereader import Reader
from cartopy.feature import NaturalEarthFeature
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.ticker as mticker

 #Abrindo shape das UFs
shp_estados= gpd.read_file('/caminho/Unidades_Federacao.shp')

estado = shp_estados[shp_estados['CD_UF'] == 'código do estado']

shp_cidade = gpd.read_file('/ccaminho/Estado_Municipios.shp')

cidade = shp_cidade[shp_cidade['CD_MUN'] == 'código da cidade']


#Para fazer o gráfico de emissões de GEEs------------------------------------------------------------

  #Abrindo a planilha do SEEG
seeg= pd.read_csv('/caminho/Municipios_SEEG.csv')


  #Selecionando a cidade
cidade_gee= seeg[seeg['Cidade']=='nome da cidade (sigla do estado)'] 


  #Selecionando o recorte temporal
anos = [str(ano) for ano in range(ano_inicio, ano_fim + 1)]

  #Somando as emissões por tipo de gás durante o período solicitado acima
gas_1 = cidade_gee[cidade_gee['Gás'] == 'nome do gás do jeito que está na tabela (unidade)'][anos].sum()

gas_2 = cidade_gee[cidade_gee['Gás'] == 'nome do gás do jeito que está na tabela (unidade)'][anos].sum()

#Criando a figura--------------------------------------------------
fig = plt.figure(figsize=(13.2,8.5)) #largura, altura

# gráfico no eixo esquerdo
ax_grafico = fig.add_axes([0.08, 0.12, 0.62, 0.77])

ax_grafico.plot(anos, gas_1, linewidth=2.5, color='cor1')
ax_grafico.plot(anos, gas_2, linewidth=2.5, color='cor2')

ax_grafico.legend(frameon=True)
ax_grafico.grid(alpha=0.3)

ax_grafico.set_ylabel('Emissões (unidade)\n', fontsize=12)
ax_grafico.set_xlabel('\nAno', fontsize=12)

ax_grafico.tick_params(axis='x',rotation=45)
ax_grafico.set_xticks(anos[::2]) #pulando de 2 em 2 anos

ax_grafico.spines['top'].set_visible(False)
ax_grafico.spines['right'].set_visible(False)

ax_grafico.legend().remove()

#Adicionando legenda para identificar os estados direto na figura
gas1_legenda= mpatches.Patch(facecolor='cor1',edgecolor='black',label= 'Nome do gás 1')
gas2_legenda= mpatches.Patch(facecolor='cor2',  edgecolor='black', label='Nome do gás 2')

fig.legend(handles=[gas1_legenda, gas2_legenda],loc='upper center',
    title='Gases',title_fontsize=13,fontsize=12.5,facecolor='white',edgecolor='black',
    bbox_to_anchor=(0.65, 0.87),borderpad=0.5, labelspacing=1,handlelength=1.2,handleheight=1.2) 


# mapa de localização dos estados no eixo direito
  #Colocando o Brasil-----------------------
ax_br = fig.add_axes([0.69, 0.58, 0.39, 0.30],projection=ccrs.PlateCarree())
                #os valores representam, respectivamente: left, bottom, width, height

xmin, xmax = -75, -32  # Longitude (Oeste a Leste)
ymin, ymax = -35, 7

ax_br.set_extent([xmin, xmax, ymin, ymax], crs=ccrs.PlateCarree())

ax_br.set_facecolor('lightblue') #colorindo o fundo com azul claro para fazer o oceano

ax_br.coastlines(linewidth=0.5)

ax_br.add_feature(cfeature.LAND, facecolor='#cor') #colorindo o continente de branco

ax_br.add_feature(cfeature.BORDERS,linewidth=0.5)

shp_estados.plot(ax=ax_br, edgecolor='black',linewidth=0.5, facecolor='#cor')

estado.plot(ax=ax_br, color='#cor', edgecolor='black', linewidth=0.6) 

ax_br.set_title('Localização do estado')


#Formatando as coordenadas
ax_br.locator_params(axis='x', nbins=5)
ax_br.locator_params(axis='y', nbins=4)

ax_br.set_xticks([-70, -55, -40], crs=ccrs.PlateCarree())
ax_br.set_yticks([-30, -15, 0], crs=ccrs.PlateCarree())

  #Coordenadas para W e S usando graus
     #Para Longitude
ax_br.xaxis.set_major_formatter(FuncFormatter(lambda valor, pos: f"{int(abs(valor))}°W"))

     #Para latitude
ax_br.yaxis.set_major_formatter(FuncFormatter(lambda valor, pos: f"{int(abs(valor))}°S"))

ax_br.tick_params(axis='y', labelrotation=90) #inclinação em 90°

ax_br.tick_params(axis='both', labelsize=8)

#Barra de escala
scalebar = ScaleBar(111000,location='lower right', length_fraction=0.18,  width_fraction=0.008,
                    box_alpha=0, color='black', scale_loc='bottom',font_properties={'size': 7})

ax_br.add_artist(scalebar)

  #Adicionando o nome do oceano na lateral direita
ax_br.text(0.8, 0.13, 'Oceano\nAtlântico', transform=ax_br.transAxes,fontsize=8.3, style='italic',alpha=0.7,color='black',ha='center')


ax_cidade = fig.add_axes([0.73, 0.22, 0.25, 0.30])

ax_cidade.set_facecolor('lightblue')

  #Trecho para controlar o tamanho do estado do rj ainda que as fronteiras apareçam
xmin, ymin, xmax, ymax = estado.total_bounds

ax_cidade.set_xlim(xmin-0.3, xmax+0.3) #limites no eixo x

ax_cidade.set_ylim(ymin-0.2, ymax+0.2) #limites no eixo y


shp_estados.plot(ax=ax_cidade, edgecolor='black',linewidth=0.5, facecolor='#cor')

  #Para adicionar os nomes dos estados: lat, lon, texto, tamanho da fonte
ax_cidade.text(-44.5, -21.5, 'estado vizinho', fontsize=10)

  #Plotando
shp_cidade.plot(ax=ax_cidade, facecolor= '#cor', edgecolor='black', linewidth=0.6)

cidade.plot(ax=ax_cidade, facecolor='#cor', edgecolor='black', linewidth= 0.8)

ax_cidade.set_title('Localização do município') #se quisesse em Negrito: weight='bold'


#Formatando as coordenadas
ax_cidade.locator_params(axis='x', nbins=3) #O nbins é para a qtd aproximada de divisões para a grade no eixo x
ax_cidade.locator_params(axis='y', nbins=3)

ax_cidade.xaxis.set_major_formatter(FuncFormatter(lambda valor, pos: f"{int(abs(valor))}°W"))

ax_cidade.yaxis.set_major_formatter(FuncFormatter(lambda valor, pos: f"{int(abs(valor))}°S"))

ax_cidade.tick_params(axis='y', labelrotation=90)

ax_cidade.tick_params(axis='both', labelsize=8)

#Barra de escala
scalebar = ScaleBar(111000,location='lower right', #posição
    length_fraction=0.18, #se estiver pegando na borda
    width_fraction=0.01, #espessura da barra
    box_alpha=0, color='black', #cor
    scale_loc='bottom',font_properties={'size': 7})

ax_cidade.add_artist(scalebar)

  #Adicionando o nome do oceano na lateral direita
ax_cidade.text(0.9, 0.15, 'Oceano\nAtlântico', transform=ax_cidade.transAxes,fontsize=8.3, style='italic',alpha=0.7,color='black',ha='center')

#Adicionando legenda para identificar os estados direto na figura
br_legenda= mpatches.Patch(facecolor='#cor',edgecolor='black',label= 'Estado do ()')
estado_legenda= mpatches.Patch(facecolor='#cor',  edgecolor='black', label='Município de ()')

fig.legend(handles=[br_legenda, estado_legenda],loc='center right', title='Legenda',title_fontsize=11.5,ncol=1,fontsize=10.5, 
    edgecolor='black', bbox_to_anchor=(0.99, 0.15),borderpad=0.5, labelspacing=0.3,handlelength=1.2,handleheight=1.2) 

#-----------------------------------------------------------------------------------------------------------

fig.text(0.8, 0.025,
         'Fontes: órgão - tema (ano);\n órgão - tema (ano).\nElaborado por nome_do_autor(a) (ano).\nSistema de Referência: SIRGAS 2000.',
         fontsize=8.5, multialignment='left',linespacing=1.2,
         bbox=dict(facecolor='white',edgecolor='black',linewidth=1,boxstyle='square,pad=0.4'))


#Para moldura em volta da figura toda
fig.patches.append(Rectangle((0,0),1,1, fill=False, transform=fig.transFigure,edgecolor='black', linewidth=1.5, zorder=10))

fig.suptitle('Título Apropriado', fontsize=17.5, linespacing= 1.8,weight= 'bold', y=0.98)


#ROSA DOS VENTOS FOTO
# Carregar imagem
img_rosa = mpimg.imread('/caminho/Rosa_Ventos.png')

# Criar OffsetImage e controlar tamanho
imagebox1 = OffsetImage(img_rosa, alpha=1, zoom=0.013,resample=True)  # zoom ajusta o tamanho e resample=True mantém a qualidade
imagebox2 = OffsetImage(img_rosa, alpha=1, zoom=0.013,resample=True)

rosa_final_br = AnnotationBbox(imagebox1, (0.96, 0.86), frameon=False, xycoords='figure fraction')
rosa_final_estado = AnnotationBbox(imagebox2, (0.76, 0.48), frameon=False, xycoords='figure fraction')

ax_br.add_artist(rosa_final_br)

ax_cidade.add_artist(rosa_final_estado)


plt.savefig('/caminho/Nome_da_Figura.png', dpi=400, bbox_inches= 'tight')

plt.show()
