class AllDatacronStats:
    def __init__(self) -> None:
        self.stats = {}
        self.stats[16] = {'name': 'crit dmg %', 'type': 'float'}  # 16 (cd?)
        self.stats[17] = {'name': 'potency', 'type': 'float'}  # 17 (potency?)
        self.stats[18] = {'name': 'tenacity',
                          'type': 'float'}  # 18 (tenacity?)
        self.stats[19] = {'name': 'dodge', 'type': 'float'}  # 19 dodge
        self.stats[20] = {'name': 'deflection',
                          'type': 'float'}  # 20 deflection
        self.stats[21] = {'name': 'phys crit %',
                          'type': 'float'}  # 21 phys crit
        self.stats[22] = {'name': 'special crit %',
                          'type': 'float'}  # 22 special crit
        self.stats[23] = {'name': 'armor %', 'type': 'float'}  # 23 armor
        self.stats[24] = {'name': 'resistance %',
                          'type': 'float'}  # 24 resistance
        self.stats[25] = {'name': 'armor penetration %',
                          'type': 'float'}  # 25 arpen
        self.stats[26] = {'name': 'resistance pentration %',
                          'type': 'float'}  # 26 respen
        self.stats[27] = {'name': 'hp steal %',
                          'type': 'float'}  # 27 (hp steal?)
        self.stats[31] = {'name': 'phys dmg %',
                          'type': 'float'}  # 31 physical damage
        self.stats[32] = {'name': 'special dmg %',
                          'type': 'float'}  # 32 special damage
        self.stats[33] = {'name': 'phys acc %',
                          'type': 'float'}  # 33 phys accuracy
        self.stats[34] = {'name': 'special acc %',
                          'type': 'float'}  # 34 special accuracy
        self.stats[35] = {'name': 'phys ca %', 'type': 'float'}  # 35 phys ca
        self.stats[36] = {'name': 'special ca %',
                          'type': 'float'}  # 36 special ca
        self.stats[55] = {'name': 'hp %', 'type': 'float'}  # 55 (hp?)
        self.stats[56] = {'name': 'prot %', 'type': 'float'}  # 56 (prot?)
        self.ability_indices = (3, 6, 9)
        self.stat_indices = [x for x in self.stats]
