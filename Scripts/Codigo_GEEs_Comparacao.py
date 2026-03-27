#SCRIPT PARA EMISSÃO DE GEEs
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

#Abrindo shape de UFs
shp_estados= gpd.read_file('/caminho/Unidades_Federacao.shp')

 #selecionando o estado por seu código
estado1 = shp_estados[shp_estados['CD_UF'] == 'número do estado de interesse']
estado2= shp_estados[shp_estados['CD_UF']=='número do estado de interesse']

  # selecionando os setores que quero observar
setores = ['Agropecuária','Energia','Mudança de Uso da Terra e Floresta','Processos Industriais','Resíduos']

#Abrindo a planilha do SEEG
seeg = pd.read_excel('/caminho/Planilha_SEEG.xlsx',
    sheet_name='Consulta Estados 2024', #nome da guia na planilha que quero abrir
    skiprows=3, header=None) #para pular as 3 linhas iniciais que atrapalhariam

#Transformar a linha 1 em nomes de colunas
seeg.columns = seeg.iloc[1]

#Remover as linhas usadas como cabeçalho
seeg = seeg[2:]

#"Limpando" os nomes
seeg.columns = seeg.columns.astype(str).str.strip()

#A primeira coluna se chamará Setor
seeg = seeg.rename(columns={seeg.columns[0]: 'Setor'})

#Selecionar apenas os estados desejados
comparacao = seeg[['Setor', 'estado_1', 'estado_2']]

comparacao['Setor'] = comparacao['Setor'].astype(str).str.strip()

comparacao = comparacao.drop_duplicates(subset='Setor')

#Remover linhas sem interesse
comparacao = comparacao[comparacao['Setor'].isin(setores)]

#Converter colunas numéricas
comparacao['estado_1'] = pd.to_numeric(comparacao['estado_1'])

comparacao['estado_2'] = pd.to_numeric(comparacao['estado_2'])

#mudando de toneladas para mega toneladas
comparacao['estado_1'] = comparacao['estado_1'] / 1e6

comparacao['estado_2'] = comparacao['estado_2'] / 1e6

# manipulando os labels
comparacao['Setor'] = comparacao['Setor'].replace({
    'Mudança de Uso da Terra e Floresta': 'Mudança de Uso\nda Terra e Floresta',
    'Processos Industriais': 'Processos\nIndustriais'})


#Criando a figura--------------------------------------------------
fig = plt.figure(figsize=(10.5,6.5)) #largura, altura

# gráfico no eixo esquerdo
ax_grafico = fig.add_axes([0.075, 0.10, 0.62, 0.75])

comparacao.plot(x='Setor', kind='bar', ax=ax_grafico,
    width=0.75,color=['cor1', 'cor2'])

ax_grafico.set_ylabel('Emissões (Mt CO₂e, GWP-AR5)', fontsize=12)
ax_grafico.set_xlabel('')

#ax_grafico.set_title('Emissão de GEEs por setor: São Paulo e Mato Grosso (2024)')

ax_grafico.tick_params(axis='x', rotation=0)
ax_grafico.grid(axis='y', alpha=0.3)
ax_grafico.legend().remove()

#Adicionando legenda para identificar os estados direto na figura
estado1_legenda= mpatches.Patch(facecolor='firebrick',edgecolor='black',label= 'nome do estado1')
estado2_legenda= mpatches.Patch(facecolor='darkgreen',  edgecolor='black', label='nome do estado2')

fig.legend(handles=[estado1_legenda, estado2_legenda],loc='center right', #localização na lateral inferior direita
    title='título apropriado',title_fontsize=12, #tamanho da fonte do título da legenda
    fontsize=11, #tamanho da fonte dos nomes das regiões
    edgecolor='black', bbox_to_anchor=(0.95, 0.26), #posição certinha para controlar o afastamento da moldura
    borderpad=0.3, labelspacing=0.8,handlelength=1.2, #largura das caixinhas
    handleheight=1.2)  #altura das caixinhas



# mapa de localização dos estados no eixo direito
  #Colocando o Brasil-----------------------
ax_br = fig.add_axes([0.73, 0.35, 0.25, 0.55],projection=ccrs.PlateCarree())
                #os valores representam, respectivamente: left, bottom, width, height

xmin, xmax = -75, -32  # Longitude (Oeste a Leste)
ymin, ymax = -35, 7

ax_br.set_extent([xmin, xmax, ymin, ymax], crs=ccrs.PlateCarree())

ax_br.set_facecolor('lightblue') #colorindo o fundo com azul claro para fazer o oceano

ax_br.coastlines(linewidth=0.5)

ax_br.add_feature(cfeature.LAND, facecolor='white') #colorindo o continente de branco

ax_br.add_feature(cfeature.BORDERS,linewidth=0.5)

shp_estados.plot(ax=ax_br, edgecolor='black',linewidth=0.5, facecolor='gainsboro')

estado1.plot(ax=ax_br, color='cor1', edgecolor='black', linewidth=0.6)

estado2.plot(ax=ax_br, color= 'cor2', edgecolor='black', linewidth=0.6)

ax_br.set_title('Localização dos estados')


#Formatando as coordenadas
ax_br.locator_params(axis='x', nbins=5) #O nbins é para a qtd aproximada de divisões para a grade no eixo x
ax_br.locator_params(axis='y', nbins=4)

ax_br.set_xticks([-70, -55, -40], crs=ccrs.PlateCarree())
ax_br.set_yticks([-30, -15, 0], crs=ccrs.PlateCarree())

  #Coordenadas para W e S usando graus e minutos
     #Para Longitude
ax_br.xaxis.set_major_formatter(FuncFormatter(lambda valor, pos: f"{int(abs(valor))}°W"))

     #Para latitude
ax_br.yaxis.set_major_formatter(FuncFormatter(lambda valor, pos: f"{int(abs(valor))}°S"))

ax_br.tick_params(axis='y', labelrotation=90) #inclinação em 90°

ax_br.tick_params(axis='both', labelsize=8)  # reduz tamanho dos números de longitude e latitude

#Barra de escala
scalebar = ScaleBar(111000,location='lower right', #posição
    length_fraction=0.18, #se estiver pegando na borda
    width_fraction=0.008, #espessura da barra
    box_alpha=0, color='black', #cor
    scale_loc='bottom',font_properties={'size': 7})

ax_br.add_artist(scalebar)

  #Adicionando o nome do oceano na lateral direita
ax_br.text(0.8, 0.13, 'Oceano\nAtlântico', transform=ax_br.transAxes,fontsize=8, style='italic',alpha=0.7,color='black',ha='center')



fig.text(0.75, 0.03, 
         'Fontes: órgão - tema (ano);\nórgão - tema (ano).\nElaborado por nome_do_autor(a) (ano).\nSistema de Referência: SIRGAS 2000.',
         fontsize=8.5, multialignment='left',linespacing=1.2,
         bbox=dict(facecolor='white',edgecolor='black',linewidth=1,boxstyle='square,pad=0.4'))


#Para moldura em volta da figura toda
fig.patches.append(Rectangle((0,0),1,1, fill=False, transform=fig.transFigure,edgecolor='black', linewidth=1.5, zorder=10))

fig.suptitle('Título Apropriado', fontsize=16, linespacing= 1.8,weight= 'bold', y=0.98)

# Para colocar a grade por cima do mapa principal
ax_br.grid(True, linestyle='--',linewidth=0.4,color='black',alpha=0.4, zorder=9)

#ROSA DOS VENTOS FOTO
# Carregar imagem
img_rosa = mpimg.imread('/caminho/Rosa_Ventos.png')

# Criar OffsetImage e controlar tamanho
imagebox = OffsetImage(img_rosa, alpha=1, zoom=0.013,resample=True)  # zoom ajusta o tamanho e resample=True mantém a qualidade

rosa_final = AnnotationBbox(imagebox, (0.97, 0.81), frameon=False, xycoords='figure fraction')

ax_br.add_artist(rosa_final)

#Colocando moldura
fig.patches.append(Rectangle((0,0),1,1, fill=False, transform=fig.transFigure,edgecolor='black', linewidth=1.5, zorder=10))


plt.savefig('/caminho/Nome_Figura.png', dpi=400, bbox_inches= 'tight')

plt.show()
