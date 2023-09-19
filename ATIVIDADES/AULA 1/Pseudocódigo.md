**Var** 
    Altura, Peso, ComprimentoMembrosInferiores, CircunferenciaTornozelo, CircunferênciaPerna, CircunferenciaCoxa, CircunferenciaCintura, TempoDeSessao: **real**
    TamanhoColete: **Literal**
    SistemaLigado, TudoRealizado, RespostaFisiologica: **Booleano**

**Inicio**

**def** ColetaInformacoesAntropometricas:

    **Leia** Altura, Peso, ComprimentoMembrosInferiores, CircunferenciaTornozelo, CircunferenciaPerna, CircunferenciaCoxa, CircunferenciaCintura, TempoDeSessao

**def** ColocacaoAcessorios:

    TransferenciaCadeiraRodasParaTatame
    VestirColete

    **Se** TamanhoColete não adequado:
        ProvidenciarColeteAdequado
    **Senao**:
        AjustarTiras
        VestirAlmofadasProtecaoVirilha
        TransferenciaPacienteTabladoCadeiraRodas

**def** ConfiguracaoSistemaLokomat:

    LigarSistema

    **Se** SistemaLigado:
        CriarNovoUsuario
        InserirInformacoesAntropometricas
    **Senao**:
        LigarSistema
        VerificarFuncionamentoIntegridade
    Esteira, Guincho, Lokomat

**def** ConexaoPacienteLokomat:

    AberturaPortaAcessoDispositivo
    DeslocamentoCadeiraRodasInteriorDispositivo
    ColocarFixarBraceletesMembrosInferiores
    FixarGuinchoColete
    InicioSuspensaoPaciente
    AjustarColete
    RetirarCadeira
    SuspensaoTotal
    FecharAcessoDispositivo

    **Se** TudoRealizado:
        IniciarProtocoloCaminhada
    **Senao**:
        ConexaoPacienteLokomat

**def** IniciarProtocoloCaminhada:

    **Leia** TempoDeSessao

    IniciarMovimentoLokomat
    IniciarFuncionamentoEsteira
    IniciarApoioParcialPaciente
    ApoioTotal
    MonitoramentoCaminhada

    **Se** RespostaFisiologica boa:
        AumentarVelocidade
    **Senao**:
        ReduzirVelocidade

    **Enquanto** TempoAtual - TempoDeSessao maior que zero:
        MonitoramentoCaminhada

**def** FinalizarProtocolo:

    DesligarEsteiraELokomat
    SuspendePaciente
    AbrirAcessoDispositivo
    AcoplarCadeira
    ApoiarPacienteCadeira
    SoltarColeteGuincho
    RemoverColete
    RemoverBraceletes
    TransferirPacienteTatame
    RetirarColete
    TransferirPacienteCadeiraRodas
    TransferirPacienteTablado
    
**Fim**
