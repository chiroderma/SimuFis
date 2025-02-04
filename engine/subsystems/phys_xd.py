import numpy
import pygame
from .objs import *
from scipy import constants

class PhysXD:
    #O tamanho do passo para se utilizar no método de Euler para integrais numéricas
    dt = 0.01
    planets = list[list[Planet, int]]()
    rect_objs = list[RectObstacle]()

    #Checa se o planeta pricipal esta dentro de alguma area não permitida
    def __rect_colision_detect(self, planet : list[Planet, int]) -> GameState | None:
        if planet[1] == 0:
            for rect in self.rect_objs:
                if_collide = rect.check_collision(self.planets[0][0])

                if if_collide == GameState.GAME_WIN or if_collide == GameState.GAME_OVER:
                    return if_collide
        
        return None
    
    def __border_pass(self) -> GameState | None:
        if self.planets[0][0].body.pos[0]/10**3 < 0 or self.planets[0][0].body.pos[0]/10**3 > 1280:
            return GameState.GAME_OVER
        
        if self.planets[0][0].body.pos[1]/10**3 < 0 or self.planets[0][0].body.pos[1]/10**3 > 720:
            return GameState.GAME_OVER
        
        return None
                
    #Calcula cada uma das forças que atuam em um corpo especifico colocando o referencial no outro objeto para que não tenhamos que negar o vetor
    #Retorna a acleração resultante das forças que atuam no corpo ou retorna o estado de jogo GAME_OVER se ouve uma colisão
    def __update_force(self, planet : list[Planet, int]
                       ) -> tuple[numpy.ndarray, bool]:
        
        #Acumular as forças que são calculadas para representar a resultante
        acumulate_forces = numpy.zeros(2)

        for plt in self.planets:
            if plt[1] == planet[1] :
                continue

            absolute_distance = numpy.linalg.norm(plt[0].body.pos - planet[0].body.pos)

            #Para checar se dois planetas colidiram precisamos verificar o seguinte:
            #Dada a distancia entre o centro desses dois planetas, temos que a distancia minima para que eles não estajam colidindo é o raio do primeiro
            #mais o raio do segundo planeta (quando a distancia esta nessa situação os dois planetas estão tangentes)
            #Portanto, para qualquer distância entre planetas talque a distância entre eles é < ao raio do primeiro + raio do segundo implica uma colisão
            if absolute_distance/10**3 < planet[0].planet_radius + plt[0].planet_radius:
                return absolute_distance, True

            force_norm = (constants.G * planet[0].body.mass * plt[0].body.mass) / absolute_distance ** 2

            x_projection = force_norm * ( (plt[0].body.pos[0] - planet[0].body.pos[0] )/absolute_distance)
            y_projection = force_norm * ( (plt[0].body.pos[1] - planet[0].body.pos[1] )/absolute_distance)

            acumulate_forces[0] += x_projection
            acumulate_forces[1] += y_projection
        
        #segunda lei de newton
        return acumulate_forces/planet[0].body.mass, False

    #O que esta escrito abaixo vem do método de integrar de Verlet
    #O metódo de Stormer-Verlet para calcular velocidades é um método adequado para esse projeto por ele ser o Thanos das tecnicas de integrar a velocidade
    #O que mais importa pra nós é q ele é facilmente implementavel, rapido, e numericamente estavel. É em essência o unico metódo sano q descreve nósso sistema
    #Agora as razões matematicas do pq ele é bom são as seguintes: Ele tem revesiabilidade no tempo (ok) e preserva a forma sympletica no espaço das fases (O quwe isso significa 
    # na nossa simulação é que ele não fode com a energia do sistema, matematicamente isso tem relação com manifolds e outras coisas q eu n tenho conhecimento)
    #Ele simplesmente é melhor que o metodo de euler de integração em todos os aspectos (outros como RK4 não mantém a enegia do sistema o q fode coisas relacionadas a campos), lógo usar ele
    #Também tem o método de leapfrog só q ele é goofy
    #TODO: Explicar esse algoritimo e a teoria no relatório
    def __velocity_verlet(self
                          ) -> None | GameState:

        rect_check = self.__rect_colision_detect(self.planets[0])
        border_check = self.__border_pass()

        if rect_check != None:
            return rect_check
        
        if border_check != None:
            return border_check

        for planet in self.planets :
            planet[0].body.pos = planet[0].body.pos + planet[0].body.vel * self.dt + planet[0].body.accel * (self.dt**2 * 0.5)
            #O update forces também checa se teve colisão
            n_accel, had_colision = self.__update_force(planet)

            if had_colision:
                return GameState.GAME_OVER
            
            planet[0].body.vel = planet[0].body.vel + (planet[0].body.accel + n_accel) * (self.dt*0.5)
            planet[0].body.accel = n_accel

    #Simula a física do jogo por um pass
    #Retorna game over se algum planeta colidir (pode ser qualquer planeta, não apenas o player) ou se o planeta player for em um retangulo de perda
    #Retorna game win se o planeta chegar na area de vitória
    def update(self) -> None | GameState:
        return self.__velocity_verlet()