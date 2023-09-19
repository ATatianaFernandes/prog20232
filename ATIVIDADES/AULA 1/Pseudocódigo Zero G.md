**Inicio**

**def** PreparacaoDoPaciente:

    ColetaInformacoesAntropometricas:
        **Leia** Peso, Altura, CircunferenciaCintura
    VestirColeteSuporte
    AjustarColeteConfortavel
    AjustarSuportedePEso

InicioDeAtividades:

    **Se** PacienteProntoEConfortavel:
        RealizarAtividadesTerapeuticas
    **Senao**:
        AjustarColetenoCorpo
        CertificarSuspensãodoPaciente

MonitoramentoDeAtividades:

    **Enquanto** TempoAtual - TempoDefinido > 0:
        RealizarAtividadesTerapeuticas
        AjustarSuportePesoConformeNecessario

FinalDaSessao:

    TerapeutaVerificaProgresso
    AcoplarCadeiraMuleta
    SoltarColeteGuincho
    RemoverColete
    TransferirPacienteTatame
    RetirarColete
    
**Fim**
