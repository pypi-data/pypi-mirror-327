import os
import importlib
import inspect

class EntityRegistry:

    _entities = {}

    _dtos = {}

    _entities_ = [
        'nsj_integracao_api_entidades.entity.financas_agencias.py',
        'nsj_integracao_api_entidades.entity.financas_bancos.py',
        'nsj_integracao_api_entidades.entity.ns_configuracoes.py',
        'nsj_integracao_api_entidades.entity.ns_empresas.py',
        'nsj_integracao_api_entidades.entity.ns_estabelecimentos.py',
        'nsj_integracao_api_entidades.entity.ns_feriados.py',
        'nsj_integracao_api_entidades.entity.ns_gruposempresariais.py',
        'nsj_integracao_api_entidades.entity.ns_obras.py',
        'nsj_integracao_api_entidades.entity.persona_adiantamentosavulsos.py',
        'nsj_integracao_api_entidades.entity.persona_admissoespreliminares.py',
        'nsj_integracao_api_entidades.entity.persona_afastamentostrabalhadores.py',
        'nsj_integracao_api_entidades.entity.persona_ambientes.py',
        'nsj_integracao_api_entidades.entity.persona_avisosferiastrabalhadores.py',
        'nsj_integracao_api_entidades.entity.persona_avisospreviostrabalhadores.py',
        'nsj_integracao_api_entidades.entity.persona_beneficios.py',
        'nsj_integracao_api_entidades.entity.persona_beneficiostrabalhadores.py',
        'nsj_integracao_api_entidades.entity.persona_calculostrabalhadores.py',
        'nsj_integracao_api_entidades.entity.persona_cargos.py',
        'nsj_integracao_api_entidades.entity.persona_compromissostrabalhadores.py',
        'nsj_integracao_api_entidades.entity.persona_concessionariasvts.py',
        'nsj_integracao_api_entidades.entity.persona_condicoesambientestrabalho.py',
        'nsj_integracao_api_entidades.entity.persona_configuracoesordemcalculomovimentosponto.py',
        'nsj_integracao_api_entidades.entity.persona_configuracoesordemcalculomovimentos.py',
        'nsj_integracao_api_entidades.entity.persona_convocacoestrabalhadores.py',
        'nsj_integracao_api_entidades.entity.persona_departamentos.py',
        'nsj_integracao_api_entidades.entity.persona_dependentestrabalhadores.py',
        'nsj_integracao_api_entidades.entity.persona_dispensavalestransportestrabalhadores.py',
        'nsj_integracao_api_entidades.entity.persona_documentoscolaboradores.py',
        'nsj_integracao_api_entidades.entity.persona_emprestimostrabalhadores.py',
        'nsj_integracao_api_entidades.entity.persona_escalasfolgastrabalhadores.py',
        'nsj_integracao_api_entidades.entity.persona_eventos.py',
        'nsj_integracao_api_entidades.entity.persona_faixas.py',
        'nsj_integracao_api_entidades.entity.persona_faltastrabalhadores.py',
        'nsj_integracao_api_entidades.entity.persona_funcoes.py',
        'nsj_integracao_api_entidades.entity.persona_gestorestrabalhadores.py',
        'nsj_integracao_api_entidades.entity.persona_historicosadiantamentosavulsos.py',
        'nsj_integracao_api_entidades.entity.persona_historicos.py',
        'nsj_integracao_api_entidades.entity.persona_horariosalternativostrabalhadores.py',
        'nsj_integracao_api_entidades.entity.persona_horariosespeciais.py',
        'nsj_integracao_api_entidades.entity.persona_horarios.py',
        'nsj_integracao_api_entidades.entity.persona_instituicoes.py',
        'nsj_integracao_api_entidades.entity.persona_intervalosjornadas.py',
        'nsj_integracao_api_entidades.entity.persona_itensfaixas.py',
        'nsj_integracao_api_entidades.entity.persona_jornadas.py',
        'nsj_integracao_api_entidades.entity.persona_lotacoes.py',
        'nsj_integracao_api_entidades.entity.persona_medicos.py',
        'nsj_integracao_api_entidades.entity.persona_membroscipa.py',
        'nsj_integracao_api_entidades.entity.persona_movimentosponto.py',
        'nsj_integracao_api_entidades.entity.persona_movimentos.py',
        'nsj_integracao_api_entidades.entity.persona_mudancastrabalhadores.py',
        'nsj_integracao_api_entidades.entity.persona_niveiscargos.py',
        'nsj_integracao_api_entidades.entity.persona_outrosrecebimentostrabalhadores.py',
        'nsj_integracao_api_entidades.entity.persona_outrosrendimentostrabalhadores.py',
        'nsj_integracao_api_entidades.entity.persona_pendenciaspagamentos.py',
        'nsj_integracao_api_entidades.entity.persona_processos.py',
        'nsj_integracao_api_entidades.entity.persona_processosrubricas.py',
        'nsj_integracao_api_entidades.entity.persona_processossuspensoes.py',
        'nsj_integracao_api_entidades.entity.persona_reajustessindicatos.py',
        'nsj_integracao_api_entidades.entity.persona_reajustestrabalhadores.py',
        'nsj_integracao_api_entidades.entity.persona_rubricasapontamento.py',
        'nsj_integracao_api_entidades.entity.persona_rubricasponto.py',
        'nsj_integracao_api_entidades.entity.persona_sindicatos.py',
        'nsj_integracao_api_entidades.entity.persona_tarifasconcessionariasvts.py',
        'nsj_integracao_api_entidades.entity.persona_tarifasconcessionariasvtstrabalhadores.py',
        'nsj_integracao_api_entidades.entity.persona_tiposanexos.py',
        'nsj_integracao_api_entidades.entity.persona_tiposdocumentoscolaboradores.py',
        'nsj_integracao_api_entidades.entity.persona_tiposfuncionarios.py',
        'nsj_integracao_api_entidades.entity.persona_tiposhistoricos.py',
        'nsj_integracao_api_entidades.entity.persona_trabalhadores.py',
        'nsj_integracao_api_entidades.entity.persona_valestransportespersonalizadostrabalhadores.py',
        'nsj_integracao_api_entidades.entity.ponto_atrasosentradascompensaveistrabalhadores.py',
        'nsj_integracao_api_entidades.entity.ponto_compensacoeslancamentos.py',
        'nsj_integracao_api_entidades.entity.ponto_diascompensacoestrabalhadores.py',
        'nsj_integracao_api_entidades.entity.ponto_pagamentoslancamentos.py',
        'nsj_integracao_api_entidades.entity.ponto_pendenciascalculostrabalhadores.py',
        'nsj_integracao_api_entidades.entity.ponto_regras.py',
        'nsj_integracao_api_entidades.entity.ponto_saidasantecipadascompensaveistrabalhadores.py'
    ]

    _dtos_ = [
        'nsj_integracao_api_entidades.dto.financas_agencias.py',
        'nsj_integracao_api_entidades.dto.financas_bancos.py',
        'nsj_integracao_api_entidades.dto.ns_configuracoes.py',
        'nsj_integracao_api_entidades.dto.ns_empresas.py',
        'nsj_integracao_api_entidades.dto.ns_estabelecimentos.py',
        'nsj_integracao_api_entidades.dto.ns_feriados.py',
        'nsj_integracao_api_entidades.dto.ns_gruposempresariais.py',
        'nsj_integracao_api_entidades.dto.ns_obras.py',
        'nsj_integracao_api_entidades.dto.persona_adiantamentosavulsos.py',
        'nsj_integracao_api_entidades.dto.persona_admissoespreliminares.py',
        'nsj_integracao_api_entidades.dto.persona_afastamentostrabalhadores.py',
        'nsj_integracao_api_entidades.dto.persona_ambientes.py',
        'nsj_integracao_api_entidades.dto.persona_avisosferiastrabalhadores.py',
        'nsj_integracao_api_entidades.dto.persona_avisospreviostrabalhadores.py',
        'nsj_integracao_api_entidades.dto.persona_beneficios.py',
        'nsj_integracao_api_entidades.dto.persona_beneficiostrabalhadores.py',
        'nsj_integracao_api_entidades.dto.persona_calculostrabalhadores.py',
        'nsj_integracao_api_entidades.dto.persona_cargos.py',
        'nsj_integracao_api_entidades.dto.persona_compromissostrabalhadores.py',
        'nsj_integracao_api_entidades.dto.persona_concessionariasvts.py',
        'nsj_integracao_api_entidades.dto.persona_condicoesambientestrabalho.py',
        'nsj_integracao_api_entidades.dto.persona_configuracoesordemcalculomovimentosponto.py',
        'nsj_integracao_api_entidades.dto.persona_configuracoesordemcalculomovimentos.py',
        'nsj_integracao_api_entidades.dto.persona_convocacoestrabalhadores.py',
        'nsj_integracao_api_entidades.dto.persona_departamentos.py',
        'nsj_integracao_api_entidades.dto.persona_dependentestrabalhadores.py',
        'nsj_integracao_api_entidades.dto.persona_dispensavalestransportestrabalhadores.py',
        'nsj_integracao_api_entidades.dto.persona_documentoscolaboradores.py',
        'nsj_integracao_api_entidades.dto.persona_emprestimostrabalhadores.py',
        'nsj_integracao_api_entidades.dto.persona_escalasfolgastrabalhadores.py',
        'nsj_integracao_api_entidades.dto.persona_eventos.py',
        'nsj_integracao_api_entidades.dto.persona_faixas.py',
        'nsj_integracao_api_entidades.dto.persona_faltastrabalhadores.py',
        'nsj_integracao_api_entidades.dto.persona_funcoes.py',
        'nsj_integracao_api_entidades.dto.persona_gestorestrabalhadores.py',
        'nsj_integracao_api_entidades.dto.persona_historicosadiantamentosavulsos.py',
        'nsj_integracao_api_entidades.dto.persona_historicos.py',
        'nsj_integracao_api_entidades.dto.persona_horariosalternativostrabalhadores.py',
        'nsj_integracao_api_entidades.dto.persona_horariosespeciais.py',
        'nsj_integracao_api_entidades.dto.persona_horarios.py',
        'nsj_integracao_api_entidades.dto.persona_instituicoes.py',
        'nsj_integracao_api_entidades.dto.persona_intervalosjornadas.py',
        'nsj_integracao_api_entidades.dto.persona_itensfaixas.py',
        'nsj_integracao_api_entidades.dto.persona_jornadas.py',
        'nsj_integracao_api_entidades.dto.persona_lotacoes.py',
        'nsj_integracao_api_entidades.dto.persona_medicos.py',
        'nsj_integracao_api_entidades.dto.persona_membroscipa.py',
        'nsj_integracao_api_entidades.dto.persona_movimentosponto.py',
        'nsj_integracao_api_entidades.dto.persona_movimentos.py',
        'nsj_integracao_api_entidades.dto.persona_mudancastrabalhadores.py',
        'nsj_integracao_api_entidades.dto.persona_niveiscargos.py',
        'nsj_integracao_api_entidades.dto.persona_outrosrecebimentostrabalhadores.py',
        'nsj_integracao_api_entidades.dto.persona_outrosrendimentostrabalhadores.py',
        'nsj_integracao_api_entidades.dto.persona_pendenciaspagamentos.py',
        'nsj_integracao_api_entidades.dto.persona_processos.py',
        'nsj_integracao_api_entidades.dto.persona_processosrubricas.py',
        'nsj_integracao_api_entidades.dto.persona_processossuspensoes.py',
        'nsj_integracao_api_entidades.dto.persona_reajustessindicatos.py',
        'nsj_integracao_api_entidades.dto.persona_reajustestrabalhadores.py',
        'nsj_integracao_api_entidades.dto.persona_rubricasapontamento.py',
        'nsj_integracao_api_entidades.dto.persona_rubricasponto.py',
        'nsj_integracao_api_entidades.dto.persona_sindicatos.py',
        'nsj_integracao_api_entidades.dto.persona_tarifasconcessionariasvts.py',
        'nsj_integracao_api_entidades.dto.persona_tarifasconcessionariasvtstrabalhadores.py',
        'nsj_integracao_api_entidades.dto.persona_tiposanexos.py',
        'nsj_integracao_api_entidades.dto.persona_tiposdocumentoscolaboradores.py',
        'nsj_integracao_api_entidades.dto.persona_tiposfuncionarios.py',
        'nsj_integracao_api_entidades.dto.persona_tiposhistoricos.py',
        'nsj_integracao_api_entidades.dto.persona_trabalhadores.py',
        'nsj_integracao_api_entidades.dto.persona_valestransportespersonalizadostrabalhadores.py',
        'nsj_integracao_api_entidades.dto.ponto_atrasosentradascompensaveistrabalhadores.py',
        'nsj_integracao_api_entidades.dto.ponto_compensacoeslancamentos.py',
        'nsj_integracao_api_entidades.dto.ponto_diascompensacoestrabalhadores.py',
        'nsj_integracao_api_entidades.dto.ponto_pagamentoslancamentos.py',
        'nsj_integracao_api_entidades.dto.ponto_pendenciascalculostrabalhadores.py',
        'nsj_integracao_api_entidades.dto.ponto_regras.py',
        'nsj_integracao_api_entidades.dto.ponto_saidasantecipadascompensaveistrabalhadores.py'
    ]

    def entity_for(self, entity_name: str):
        if len(self._entities)==0:
            for nome_modulo in self._entities_:
                modulo = importlib.import_module(nome_modulo)
                s = modulo.removeprefix("nsj_integracao_api_entidades.entity.").removesuffix(".py")
                # Substitui o primeiro "_" por "."
                partes = s.split("_", 1)
                _tabela = ".".join(partes) if len(partes) == 2 else s
                for _nome, _classe in inspect.getmembers(modulo, inspect.isclass):
                    if _classe.__module__ == nome_modulo:
                        self._entities[_tabela] = _classe

        _classe = self._entities.get(entity_name)
        if _classe is None:
            raise KeyError(f"Não existe uma Entidade correpondente a tabela {entity_name}")

        return _classe

    def dto_for(self, entity_name: str):
        if len(self._dtos)==0:
            for nome_modulo in self._dtos_:
                modulo = importlib.import_module(nome_modulo)
                s = modulo.removeprefix("nsj_integracao_api_entidades.dto.").removesuffix(".py")
                # Substitui o primeiro "_" por "."
                partes = s.split("_", 1)
                _tabela = ".".join(partes) if len(partes) == 2 else s
                for _nome, _classe in inspect.getmembers(modulo, inspect.isclass):
                    if _classe.__module__ == nome_modulo:
                        self._dtos[_tabela] = _classe

        _classe = self._dtos.get(entity_name)
        if _classe is None:
            raise KeyError(f"Não existe um DTO correpondente a tabela {entity_name}")

        return _classe

    def entity_for_v2(self, entity_name: str):
        if len(self._entities)==0:
            for files in os.listdir(os.path.join(os.path.dirname(__file__), 'entity')):
            #for files in os.listdir(f"{os.getcwd()}/entity/"):
                if files.endswith('.py') and files!='__init__.py':
                    nome_modulo = f'nsj_integracao_api_entidades.entity.{files[:-3]}'
                    modulo = importlib.import_module(nome_modulo)
                    for _nome, _classe in inspect.getmembers(modulo, inspect.isclass):
                        if _classe.__module__ == nome_modulo:
                            self._entities[files[:-3].replace('_','.')] = _classe

        _classe = self._entities.get(entity_name)
        if _classe is None:
            raise KeyError(f"Não existe uma Entidade correpondente a tabela {entity_name}")

        return _classe

    def dto_for_v2(self, entity_name: str):
        if len(self._dtos)==0:
            #for files in os.listdir(f"{os.getcwd()}/dto/"):
            for files in os.listdir(os.path.join(os.path.dirname(__file__), 'dto')):
                if files.endswith('.py') and files!='__init__.py':
                    nome_modulo = f'nsj_integracao_api_entidades.dto.{files[:-3]}'
                    modulo = importlib.import_module(nome_modulo)
                    for _nome, _classe in inspect.getmembers(modulo, inspect.isclass):
                        if _classe.__module__ == nome_modulo:
                            self._dtos[files[:-3].replace('_','.')] = _classe

        _classe = self._dtos.get(entity_name)
        if _classe is None:
            raise KeyError(f"Não existe um DTO correpondente a tabela {entity_name}")

        return _classe