######### IMPORTANDO BIBLIOTECAS ###########
import geopandas as gpd
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
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.ticker as mticker


#Abrindo shape dos estados do Brasil
shp_biomas=  gpd.read_file('/caminho/arq-biomas-ibge.shp')

#Abrindo shape dos estados do país
shape_estados= gpd.read_file('/caminho/arq-unidades-da-federacao-ibge.shp')

#SHP do Brasil
regioes_shape = gpd.read_file('/caminho/arq-regioes-br.shp')

biomas_unidos = shp_biomas.dissolve(by='nm_bm') #nome da coluna que corresponde aos biomas

# Definir cores por região
cores_biomas = {"nome do bioma da forma que está escrito na coluna do shp": "#cor"}

#Para preencher os biomas do Brasil de acordo com a paleta escolhida acima
biomas_unidos['cor'] = biomas_unidos.index.map(cores_biomas)

shp_transicao = shp_biomas[shp_biomas['nm_dm_nat'] == 'nome de interesse e igual ao que está na coluna do shp']

transicao_unida = shp_transicao.dissolve(by='nm_dm_nat') #nome da coluna que corresponde aos domínios naturais

transicao_unida['cor']= 'lightgray' #cor para as áreas de transição

#CRIANDO A FIGURA---------------------------------------------------------------------------------------
  #Tamanho da Figura = proporcional para mostrar o Brasil em destaque
fig = plt.figure(figsize=(8.8, 8.5)) #largura, altura
ax = fig.add_axes([0.04, 0.05, 0.75, 0.94], projection=ccrs.PlateCarree()) #left, bottom, width, height

xmin, xmax = -75, -32  # Longitude (Oeste a Leste)
ymin, ymax = -35, 7    # Latitude (Sul a Norte)

ax.set_extent([xmin, xmax, ymin, ymax], crs=ccrs.PlateCarree())

# Fronteiras entre países e costa
ax.add_feature(cfeature.BORDERS, linewidth=1.0, edgecolor='black', alpha=0.8, zorder=7)

ax.coastlines(linewidth=1.0, edgecolor='black', alpha=0.8, zorder=7)

ax.add_feature(cfeature.LAND, facecolor='whitesmoke') #colorindo o continente de branco fumaça

#Plotando os biomas e áreas de transição no mapa com as cores escolhidas
biomas_unidos.plot(ax=ax, color=biomas_unidos['cor'],zorder=3)

transicao_unida.plot(ax=ax,color=transicao_unida['cor'],edgecolor='none',alpha=0.9,zorder=4, hatch='///')
      #as áreas de transição ficam com hachurado


# Colocando os limites das regiões brasileiros
regioes_shape.boundary.plot(ax=ax, edgecolor='black',color='black',linewidth=1.2,alpha=0.85, zorder=5)

ax.set_facecolor('lightblue') #colorindo o fundo de azul claro

#Barra de escala
scalebar = ScaleBar(111000,location='lower right', #posição
    length_fraction=0.18, #se estiver pegando na borda
    width_fraction=0.008, #espessura da barra
    box_alpha=0, color='black', #cor
    scale_loc='bottom',font_properties={'size': 9})

ax.add_artist(scalebar)


#Pra criar a legenda com as cores das regiões no canto inferior direito
  #associando cores para as caixinhas, e colocando o nome da região ao lado
nome_do_bioma = mpatches.Patch(facecolor='#cod-da-cor',  edgecolor='black', label='Nome do Bioma')

fig.legend(handles=[nome_do_bioma],loc='lower right', #localização na lateral inferior direita
    title='título da legenda',title_fontsize=12.5, #tamanho da fonte do título da legenda
    fontsize=11, #tamanho da fonte dos itens da legenda
    edgecolor='black',
    bbox_to_anchor=(0.99, 0.012), #posição certinha para controlar o afastamento da moldura
    borderpad=0.3,
    labelspacing=0.8,
    handlelength=1.2, #largura das caixinhas
    handleheight=1.2)  #altura das caixinhas

#Pra adicionar os nomes das regiões em cima dos recortes
  #encontrando o ponto central representativo de cada estado
regioes_shape['centroide'] = regioes_shape.geometry.representative_point()
regioes_shape['x'] = regioes_shape.centroide.x
regioes_shape['y'] = regioes_shape.centroide.y

#associando as siglas dos estados com seus polígonos
nomes = {'nome da região igual o jeito que está no shape de regiões': 'nome como quero que fique'}

for idx, row in regioes_shape.iterrows():
    ax.text(row['x'], row['y'], nomes[row['NM_REGIAO']], ha='center', fontsize=10, fontweight='bold',
            path_effects=[pe.withStroke(linewidth=3.5, foreground="white")], zorder=10)

#Para adicionar os nomes dos oceanos nas laterais
ax.text(-72.5, -22, 'nome do oceano', transform=ccrs.PlateCarree(),fontsize=10,style='italic', alpha=0.7,ha='center')
      #posição no eixo x, posição no eixo y

ax.text(-36, -28, 'nome do oceano', #com coordenadas para posicionar o texto e qual texto quer adicionar
        transform=ccrs.PlateCarree(),fontsize=12, #tamanho da fonte
        style='italic', #estilo da fonte
        alpha=0.7,ha='center') #posição central

#Legenda de autoria e referência-----------------------------
  #Criando a caixa para legenda
caixa_legenda= mpatches.Patch(color='white', edgecolor='black')

fig.text(0.03, 0.025, #posição no eixo x, e posição no eixo y
         'Fonte: Órgão – item (ano); item (ano).\nElaborado por nome do(a) autor(a) (ano).\nSistema: ex-> SIRGAS 2000.',
         fontsize=10, multialignment='left', #para alinhar todo o texto da legenda à esquerda
         bbox=dict(facecolor='white',edgecolor='black',linewidth=1,boxstyle='square,pad=0.6'))


#Para moldura em volta da figura toda
fig.patches.append(Rectangle((0,0),1,1, fill=False, transform=fig.transFigure,edgecolor='black', linewidth=1.5, zorder=10))

#Título
fig.suptitle('Título Apropriado', fontsize=18, weight= 'bold', y=0.98)

# Grade de coordenadas
gl = ax.gridlines(draw_labels=True, x_inline=False, y_inline=False, linestyle='--',linewidth=0.4, alpha=0.8, color='gray')
gl.xlines = True  #desenha as linhas verticais
gl.ylines = True  #desenha as linhas horizontais
gl.top_labels = False
gl.right_labels = False
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
gl.xlabel_style = {'fontsize': 8} #controlando o tamanho da fonte das coordenadas
gl.ylabel_style = {'fontsize': 8}

  #controlando o intervalo entre as coordenadas
gl.xlocator = mticker.FixedLocator([-70, -60, -50, -40]) # Longitude
gl.ylocator = mticker.FixedLocator([-30, -15, 0]) # Latitude

  # Rotação específica para os números da latitude (eixo Y)
gl.ylabel_style = {'rotation': 90}

#Adicionando a Rosa dos Ventos a partir de uma imagem de autoria própria
  #Carregando a imagem
img_rosa = mpimg.imread('/caminho/Rosa_Ventos.png')

# Criar OffsetImage e controlar tamanho da figura
imagebox = OffsetImage(img_rosa, alpha=1, zoom=0.048,resample=True)  
      # zoom ajusta o tamanho, e resample=True mantém a qualidade da imagem

# Posicionar na figura
rosa_final = AnnotationBbox(imagebox, (0.89, 0.85), frameon=False, xycoords='figure fraction')

ax.add_artist(rosa_final) #adicionando em relação ao eixo

#Salvando
plt.savefig('/caminho/Biomas_Br.png', dpi=500, bbox_inches='tight')
        #dpi é a qualidade da imagem
