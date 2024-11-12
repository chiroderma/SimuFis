from .subsystems.objs import *
from .subsystems.phys_xd import *
from .subsystems.rendering import *

class GameEngine:
    #não é necessario essa lista, mas se acabar sendo necessario ela esta aqui
    #É uma lista de planetas e id de cada um
    #O planeta de index/id 0 é o planeta principal
    planets = list[list[Planet, int]]()
    rect_objs = list[RectObstacle]()

    def __init__(self) -> None:
        pygame.init()
        self.physXD = PhysXD()
        #Eu lockei essa resolução para que tudo que tudo mundo fazer fique padronizado e funcionando
        self.render_sistem = Renderer(1280, 720)

    def add_planet(self, planet : Planet) -> None:
        if not self.planets:
            self.planets.append([planet, 0])
            self.physXD.planets.append([planet, 0])
            self.render_sistem.planets.append([planet, 0])
        else:
            #Acessando o id do ultimo planeta e adicionando mais 1 para o próximo id
            next_id_value = self.planets[-1][1] + 1
            self.planets.append([planet, next_id_value])
            self.physXD.planets.append([planet, next_id_value])
            self.render_sistem.planets.append([planet, next_id_value])
    
    #Adiciona um objeto de retangulo na game engine
    def add_rect_obstacle(self, obstacle : RectObstacle) -> None:
        self.rect_objs.append(obstacle)
        self.physXD.rect_objs.append(obstacle)
        self.render_sistem.rect_objs.append(obstacle)

    #Muda as caracteristacas de um planeta
    def change_planet_characteristics(self, planet_id : int, **kwargs) -> None :
        if 'vel' in kwargs:
            self.planets[planet_id] = numpy.array(kwargs['vel'])

    def update_physics(self) -> None:
        self.physXD.update()
    
    def render(self) -> None:
        self.render_sistem.render(GameState.SIMULATE)

    #Deleta todos os objetos de todas os módulos da engine
    def __delete_all_objs(self) -> None:
        self.planets.clear()
        self.physXD.planets.clear()
        self.render_sistem.planets.clear()
        self.rect_objs.clear()
        self.physXD.rect_objs.clear()
        self.render_sistem.rect_objs.clear()

    #Transforma os objetos que foi colocados até agora em um nível.
    def to_level(self, level_number : int) -> None:
        with open(f'./engine/levels/{level_number}.lv', 'w') as lv:
            for planet in self.planets:
                #Simplesmente escreve todos os dados do planeta do nível que vc tinha criado
                lv.write(f'planet {planet[0].body.mass/10**3} {planet[0].body.pos[0]/10**3} {planet[0].body.pos[1]/10**3} {planet[0].body.vel[0]} {planet[0].body.vel[1]} {planet[0].body.accel[0]} {planet[0].body.accel[1]} {planet[0].planet_radius} {planet[0].color[0]} {planet[0].color[1]} {planet[0].color[2]} {planet[0].color[3]}\n')

            for rect in self.rect_objs:
                #Escreve todos os dados do retangulo em um arquivo
                lv.write(f'rect {rect.width} {rect.height} {rect.pos[0]} {rect.pos[1]} {rect.type} {rect.color[0]} {rect.color[1]} {rect.color[2]} {rect.color[3]}')


    #Carrega todos os objetos contidos em um nivel arquivo de nível
    #deletando os que estavam presentes no momento
    def load_level(self, level_number : int) -> None:
        self.__delete_all_objs()
        with open(f'./engine/levels/{level_number}.lv', 'r') as lv:
            #Cada linha vai conter os dados de um planeta/rect em que a primeira palavra ira indicar se é um planeta ou um rect
            for line in lv:
                data = line.split()

                if data[0] == 'planet':
                    #Coloca manualmente os dados do planeta e adiciona ele
                    planet_to_add = Planet(float(data[1]), [float(data[2]), float(data[3])], [float(data[4]), float(data[5])], [float(data[6]), float(data[7])], float(data[8]), [int(data[9], 10), int(data[10], 10), int(data[11], 10), int(data[12], 10)])
                    self.add_planet(planet_to_add)

                else:
                    #assim como o planeta coloca os dados manualmente no objeto de retangulo
                    rect_to_add = RectObstacle(float(data[1]), float(data[2]), [float(data[3]), float(data[4])], int(data[5], 10), [int(data[6], 10), int(data[7], 10), int(data[8],10), int(data[9],10)])
                    self.add_rect_obstacle(rect_to_add)
                