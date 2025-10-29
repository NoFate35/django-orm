https://docs.djangoproject.com/en/5.2/topics/db/models/#intermediary-manytomany

https://docs.djangoproject.com/en/5.2/topics/db/models/#intermediary-manytomany



        print('island', island. name, 'by_ship', by_ship.name, 'self', self.name)
        island_a = self
        island_b = island
        ship = by_ship
        way = Ship.objects.filter(islands=island_a).filter(islands=island_b)
        print('way', way)

        return(bool(way))
