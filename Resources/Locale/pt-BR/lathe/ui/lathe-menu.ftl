lathe-menu-connected-to-silo-message = Connected to material silo.
lathe-menu-reagent-slot-examine = It has a slot for a beaker on the side.
lathe-menu-title = Menu do Torno
lathe-reagent-dispense-no-container = Liquid pours out of { THE($name) } onto the floor!
lathe-menu-result-reagent-display = { $reagent } ({ $amount }u)
lathe-menu-queue = Fila
lathe-menu-server-list = Servidores
lathe-menu-sync = Sincronizar
lathe-menu-search-designs = Procurar Projetos
lathe-menu-category-all = Todos
lathe-menu-search-filter = Filtrar
lathe-menu-amount = Quantidade:
lathe-menu-material-display = { $material } ({ $amount })
lathe-menu-tooltip-display = { $amount } de { $material }
lathe-menu-description-display = [italic]{ $description }[/italic]
lathe-menu-material-amount =
    { $amount ->
        [1] { NATURALFIXED($amount, 2) } { $unit }
       *[other] { NATURALFIXED($amount, 2) } { MAKEPLURAL($unit) }
    }
lathe-menu-material-amount-missing =
    { $amount ->
        [1] { NATURALFIXED($amount, 2) } { $unit } of { $material } ([color=red]{ NATURALFIXED($missingAmount, 2) } { $unit } missing[/color])
       *[other] { NATURALFIXED($amount, 2) } { MAKEPLURAL($unit) } of { $material } ([color=red]{ NATURALFIXED($missingAmount, 2) } { MAKEPLURAL($unit) } missing[/color])
    }
lathe-menu-no-materials-message = Nenhum material carregado.
lathe-menu-fabricating-message = Fabricando...
lathe-menu-materials-title = Materiais
lathe-menu-queue-title = Fila de construção
