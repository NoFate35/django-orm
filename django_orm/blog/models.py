from django.db import models


class Island(models.Model):
    name = models.CharField(max_length=200)

    def can_reach(self, island, *, by_ship):
        "Return True if one can reach the @island using a @by ship"
        # BEGIN (write your solution here)
        print('island', island. name, 'by_ship', by_ship.name, 'self', self.name)
        island_a = self
        island_b = island
        ship = by_ship
        way = Ship.objects.filter(islands=island_a).filter(islands=island_b)
        print('way', way)

        return(bool(way))
        # END


class Ship(models.Model):
    name = models.CharField(max_length=200)
    islands = models.ManyToManyField(Island, related_name='ships')