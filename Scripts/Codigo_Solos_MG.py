#IMPORTANDO BIBLIOTECAS
import geopandas as gpd
import matplotlib.pyplot as plt
import shapely
from matplotlib_scalebar.scalebar import ScaleBar
from matplotlib.patches import Rectangle
import matplotlib.patches as mpatches
from matplotlib.ticker import FuncFormatter
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

#Abrindo shape do Brasil
brasil = gpd.read_file('/caminho/BR_arq.shp')

#Abrindo shape as UFs
shp_estados= gpd.read_file('/caminho/Unidades_Federacao.shp')

 #selecionando o estado por seu código
estado = shp_estados[shp_estados['CD_UF'] == 'número que corresponde ao código do estado desejado dentro dos shp de UFs']

#Abrindo shp dos solos
shp_solos = gpd.read_file('/caminho/pedo_area.shp').to_crs("EPSG:4326")

#Juntando as classes de solos

solos_sel= shp_solos.loc[shp_solos['ordem'].isin(['LATOSSOLO','ARGISSOLO','CAMBISSOLO','GLEISSOLO','NEOSSOLO',
                                                  'ORGANOSSOLO', 'PLANOSSOLO','AFLORAMENTOS DE ROCHAS',
                                                  'DUNAS', 'ESPODOSSOLO', 'NITOSSOLO', 'LUVISSOLO',
                                                  'NITOSSOLO','PLINTOSSOLO','CHERNOSSOLO','VERTISSOLO', 'None'])].copy()

solos_sel_corrigido= gpd.GeoDataFrame(solos_sel, geometry='geometry',crs=shp_solos.crs) #transformando em GeoDataFrame de novo

solos_sel_corrigido['geometry']= solos_sel_corrigido.geometry.buffer(0) #removendo vazios internos

solos_unidos= solos_sel_corrigido.dissolve(by='ordem')

solos_unidos= solos_unidos.reset_index()

# Definir cores por região
cores_solos = {"LATOSSOLO": "#cor","ARGISSOLO": "#cor",
               "NEOSSOLO": "#cor","GLEISSOLO": "#cor",
               "CAMBISSOLO": "#cor", "ORGANOSSOLO": "#cor",
               "PLANOSSOLO": "#cor", "NITOSSOLO": "#cor",
               "AFLORAMENTOS DE ROCHAS": "#cor", "DUNAS": "#cor",
               "ESPODOSSOLO": '#cor', 'LUVISSOLO': '#cor',
               "PLINTOSSOLO":'#cor', "CHERNOSSOLO":'#cor',
               "VERTISSOLO": '#cor', 'None':'#cor'}

#Para preencher os tipos de solo com as cores de acordo com a paleta escolhida acima
solos_unidos['cor'] = solos_unidos['ordem'].map(cores_solos).fillna('white')

solos_unidos['geometry'] = solos_unidos['geometry'].buffer(0)

solos_estado = gpd.clip(solos_unidos, estado)


#---------------------CRIANDO A FIGURA---------------------------------
fig= plt.figure(figsize=(12,8.3)) #largura, comprimento


#MAPA do estado------------------------------
ax = fig.add_axes([0.03, 0.17, 0.63, 0.75])
                #os valores representam, respectivamente: left, bottom, width, height

ax.set_facecolor('lightblue')

  #Trecho para controlar o tamanho do estado
xmin, ymin, xmax, ymax = mg.total_bounds

ax.set_xlim(xmin-0.2, xmax+0.2) #limites no eixo x
ax.set_ylim(ymin-0.1, ymax+0.1) #limites no eixo y

shp_estados.plot(ax=ax, edgecolor='black', linewidth=1.2,facecolor='gainsboro')

solos_estado.plot(ax=ax, color= solos_estado['cor'], edgecolor='none', zorder=3) 

estado.plot(ax=ax, color='none',edgecolor='black', linewidth=1.2, zorder=4)

  #Para adicionar os nomes dos estados: lat, lon, texto, tamanho da fonte
ax.text(-42.5, -22.5, 'sigla do estado', fontsize=13)


#Formatando as coordenadas
ax.locator_params(axis='x', nbins=3)
ax.locator_params(axis='y', nbins=4)

#Para Longitude
ax.xaxis.set_major_formatter(FuncFormatter(lambda valor, pos: f"{int(abs(valor))}°W"))

#Para latitude
ax.yaxis.set_major_formatter(FuncFormatter(lambda valor, pos: f"{int(abs(valor))}°S"))

ax.tick_params(axis='y', labelrotation=90) #inclinação em 90°

ax.tick_params(axis='both', labelsize=8)


#Barra de escala
scalebar = ScaleBar(111000,location='lower right', length_fraction=0.18,
                    width_fraction=0.008, box_alpha=0,color='black',
                    scale_loc='bottom',font_properties={'size': 9.3})

ax.add_artist(scalebar)

#Adicionando nome do Oceano
ax.text(0.94, 0.14, 'Oceano\nAtlântico',transform=ax.transAxes,fontsize=11,
        style='italic',alpha=0.7,color='black',rotation=26, ha='center', zorder= 6)


#MAPA NO EIXO À DIREITA------------------------------------------

  #Colocando o Brasil-----------------------
ax_br = fig.add_axes([0.68, 0.35, 0.37, 0.37],projection=ccrs.PlateCarree())
                #os valores representam, respectivamente: left, bottom, width, height

xmin, xmax = -75, -32  # Longitude (Oeste a Leste)
ymin, ymax = -35, 7

ax_br.set_extent([xmin, xmax, ymin, ymax], crs=ccrs.PlateCarree())

ax_br.set_facecolor('lightblue') #colorindo o fundo com azul claro para fazer o oceano

ax_br.coastlines(linewidth=0.5)

ax_br.add_feature(cfeature.LAND, facecolor='white') #colorindo o continente de branco

ax_br.add_feature(cfeature.BORDERS,linewidth=0.5)

shp_estados.plot(ax=ax_br, edgecolor='black',linewidth=0.5, facecolor='gainsboro')

estado.plot(ax=ax_br, color='#cb4cf5', edgecolor='black', linewidth=0.6)

ax_br.set_title('Título apropriado')


#Formatando as coordenadas
ax_br.locator_params(axis='x', nbins=5)
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

  #Adicionando o nome do oceano na lateral direita
ax_br.text(0.8, 0.1, 'Oceano\nAtlântico', transform=ax_br.transAxes,fontsize=8.7, style='italic',alpha=0.7,color='black',ha='center') #posição central


#Título no mapa------------------------------------
fig.suptitle('Título apropriado', fontsize=16, weight= 'bold', y=0.98)


#Legenda de autoria e referência-----------------------------
caixa_legenda= mpatches.Patch(color='white', edgecolor='black')

#0.96 no primeiro argumento caso eu queira manter no canto inferior direito
fig.text(0.02, 0.03, 'Fonte: órgão - assunto (ano).\nElaborado por autor(a) (ano).\nSistema: SIRGAS 2000.',fontsize=10,multialignment='left',bbox=dict(facecolor='white',edgecolor='black',linewidth=1,boxstyle='square,pad=0.6'))


#Para moldura em volta da figura toda
fig.patches.append(Rectangle((0,0),1,1, fill=False, transform=fig.transFigure,edgecolor='black', linewidth=1.5, zorder=10))


#Legenda para os mapas
caixa_br = mpatches.Patch(facecolor='#cb4cf5', edgecolor='black', label='legenda apropriada')

fig.legend(handles=[caixa_br],title='Legenda',title_fontsize=12,fontsize=11.5,loc='upper right',
           bbox_to_anchor=(1, 0.31),borderpad=0.5,edgecolor='black',labelspacing=0.5,
           handlelength=1.2, handleheight=1.2)  #altura das caixinhas


tipo_de_solo1= mpatches.Patch(facecolor='red',  edgecolor='black', label='Tipo 1')

fig.legend(handles=[tipo_de_solo1, tipo_de_solo2, tipo_de_solo3, tipo_de_solo4],
           title='Título apropriado',title_fontsize=13,fontsize=11,loc='lower right',
           ncol = 4, columnspacing= 0.8, bbox_to_anchor=(1, 0.005),borderpad=0.3,edgecolor='black', labelspacing=0.5,
           handlelength=1.2,handleheight=1.2)
         

# Para colocar a grade por cima do mapa principal
ax.grid(True, linestyle='--',linewidth=0.4,color='black',alpha=0.4, zorder=9)

#ROSA DOS VENTOS FOTO
# Carregar imagem
img_rosa = mpimg.imread('/caminho/Rosa_Ventos.png')

# Criar OffsetImage e controlar tamanho
imagebox = OffsetImage(img_rosa, alpha=1, zoom=0.04,resample=True)  # zoom ajusta o tamanho e resample=True mantém a qualidade

# Posicionar na figura (valores 0-1 são fração da figura)
rosa_final = AnnotationBbox(imagebox, (0.72, 0.86), frameon=False, xycoords='figure fraction')

ax.add_artist(rosa_final)

plt.savefig('/caminho/Nome_da_Figura.png', dpi=400, bbox_inches= 'tight')

plt.show()
