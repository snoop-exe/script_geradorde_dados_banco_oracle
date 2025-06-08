from faker import Faker
import random
import oracledb

def conectar_banco():
    # Exemplo de conexão com oracledb, ajuste host, porta, serviço, usuário e senha
    dsn = oracledb.makedsn( "localhost",1521, service_name="XEPDB1")
    conexao = oracledb.connect(user="clinica_geral", password="uniube", dsn=dsn)
    return conexao

QTD = 100



fake = Faker('pt_BR')




def gerar_pessoas():
    # 1 - PESSOAS
    pessoas_inserts = []
    for i in range(200):
        nome = fake.name().replace("'", "''")
        data_nasc = fake.date_of_birth(minimum_age=0, maximum_age=90).strftime('%d-%m-%Y')
        endereco = fake.address().replace('\n', ', ').replace("'", "''")
        telefone = fake.phone_number().replace("'", "''")
        email = fake.unique.email().replace("'", "''")
        insert = f"INSERT INTO PESSOAS (nome, data_nascimento, endereco, telefone, email) VALUES ('{nome}', TO_DATE('{data_nasc}', 'DD-MM-YYYY'), '{endereco}', '{telefone}', '{email}')"
        pessoas_inserts.append(insert)
    return pessoas_inserts

def gerar_departamento():
    # 2 - DEPARTAMENTO
    departamentos = ['Administração', 'Financeiro', 'Recursos Humanos', 'TI', 'Atendimento', 'Limpeza', 'Segurança',
                     'Enfermagem', 'Farmácia', 'Recepção']
    departamento_inserts = []
    qntd_departamentos = len(departamentos)
    for i in range(qntd_departamentos):
        nome_dep = departamentos[i].replace("'", "''")  # Pega o departamento na ordem, sem repetir
        insert = f"INSERT INTO DEPARTAMENTO (nome_departamento) VALUES ('{nome_dep}')"
        departamento_inserts.append(insert)
    return departamento_inserts


def gerar_funcionario():
    # 3 - FUNCIONARIO
    funcionario_inserts = []
    cargos = [
        'Recepcionista', 'Auxiliar Administrativo', 'Enfermeiro',
        'Técnico de Enfermagem', 'Fisioterapeuta', 'Psicólogo',
        'Nutricionista', 'Farmacêutico', 'Gerente de Clínica',
        'Coordenador de Atendimento'
    ]
    for i in range(50):
        id_pessoa = 1 + i
        id_departamento = random.randint(1,10)
        cargo = random.choice(cargos).replace("'", "''")
        data_contrat = fake.date_between(start_date='-10y', end_date='today').strftime('%d-%m-%Y')
        salario = round(random.uniform(2000, 10000), 2)
        insert = f"INSERT INTO FUNCIONARIO (id_pessoa, id_departamento, cargo, data_contratacao, salario) VALUES ({id_pessoa}, {id_departamento}, '{cargo}', TO_DATE('{data_contrat}', 'DD-MM-YYYY'), {salario})"
        funcionario_inserts.append(insert)
    return funcionario_inserts
def gerar_especialidades():
    # 4 - ESPECIALIDADE
    especialidades = ['Cardiologia', 'Dermatologia', 'Pediatria', 'Ortopedia', 'Neurologia', 'Ginecologia',
                      'Psiquiatria', 'Oftalmologia', 'Endocrinologia', 'Urologia']
    especialidade_inserts = []
    qntd_especialidades = len(especialidades)
    for i in range(qntd_especialidades):
        nome_esp = especialidades[i].replace("'", "''")
        insert = f"INSERT INTO ESPECIALIDADE (nome_especialidade) VALUES ('{nome_esp}')"
        especialidade_inserts.append(insert)
    return  especialidade_inserts


def gerar_medico():
    medico_inserts = []
    update_funcionario_medicos = []

    ids_funcionarios = list(range(1, 50))
    ids_medicos = random.sample(ids_funcionarios, 20)

    cargos_medicos = 'Médico'

    for id_pessoa in ids_medicos:
        id_especialidade = random.randint(11, 20)
        crm = fake.unique.bothify(text='??######').replace("'", "''")

        # Insert na tabela MEDICO
        insert = (
            f"INSERT INTO MEDICO (id_pessoa, id_especialidade, crm) "
            f"VALUES ({id_pessoa}, {id_especialidade}, '{crm}')"
        )
        medico_inserts.append(insert)

        # Atualização do salário e cargo na tabela FUNCIONARIO
        novo_cargo = cargos_medicos
        novo_salario = round(random.uniform(12000, 25000), 2)
        for i in ids_medicos:
            update = (
                f"UPDATE FUNCIONARIO SET cargo = '{novo_cargo}', salario = {novo_salario} "
                f"WHERE id_funcionario = {i}"
            )
            update_funcionario_medicos.append(update)

    return medico_inserts + update_funcionario_medicos


def gerar_convenio():
    # 6 - CONVENIO
    convenios = ['Unimed', 'Bradesco Saúde', 'Amil', 'SulAmérica', 'Porto Seguro', 'Notredame', 'Assim', 'Hapvida',
                 'Prevent Senior', 'Care Plus']
    qntd_convenios = len(convenios)
    convenio_inserts = []
    for i in range(qntd_convenios):
        nome_conv =  convenios[i].replace("'","''")
        descricao = f"Convênio de saúde {nome_conv}".replace("'", "''")
        insert = f"INSERT INTO CONVENIO (nome_convenio, descricao) VALUES ('{nome_conv}', '{descricao}')"
        convenio_inserts.append(insert)
    return convenio_inserts

def gerar_paciente():
    # 7 - PACIENTE
    paciente_inserts = []
    for i in range(150):
        id_pessoa = 1 + i

        # 70% dos pacientes terão convênio
        tem_convenio = random.random() < 0.7

        if tem_convenio:
            id_convenio = random.randint(1, 10)
            numero_conv = fake.bothify(text='###-#####').replace("'", "''")
            insert = (
                f"INSERT INTO PACIENTE (id_pessoa, id_convenio, numero_convenio) "
                f"VALUES ({id_pessoa}, {id_convenio}, '{numero_conv}')"
            )
        else:
            insert = (
                f"INSERT INTO PACIENTE (id_pessoa, id_convenio, numero_convenio) "
                f"VALUES ({id_pessoa}, NULL, NULL)"
            )

        paciente_inserts.append(insert)

    return paciente_inserts


def gerar_consultas():
    # 8 - CONSULTAS
    consultas_inserts = []
    for i in range(QTD):
        id_medico = random.randint(1, 20)
        id_paciente = random.randint(1, 150)
        data_consulta = fake.date_time_between(start_date='-1y', end_date='now').strftime('%d-%m-%Y %H:%M:%S')
        observacoes = fake.sentence(nb_words=10).replace("'", "''")
        insert = f"INSERT INTO CONSULTAS (id_medico, id_paciente, data_consulta, observacoes) VALUES ({id_medico}, {id_paciente}, TO_TIMESTAMP('{data_consulta}', 'DD-MM-YYYY HH24:MI:SS'), '{observacoes}')"
        consultas_inserts.append(insert)
    return  consultas_inserts

def gerar_formulario():
    # 9 - FORMULARIO
    formulario_inserts = []
    for i in range(QTD):
        id_consulta = i + 1
        data_preenchimento = fake.date_between(start_date='-1y', end_date='today').strftime('%d-%m-%Y')
        conteudo = fake.text(max_nb_chars=200).replace("'", "''")
        insert = f"INSERT INTO FORMULARIO (id_consulta, data_preenchimento, conteudo) VALUES ({id_consulta}, TO_DATE('{data_preenchimento}', 'DD-MM-YYYY'), '{conteudo}')"
        formulario_inserts.append(insert)
    return formulario_inserts

def gerar_prontuario():
    # 10 - PRONTUARIO
    prontuario_inserts = []
    for i in range(QTD):
        id_paciente = i + 1
        data_criacao = fake.date_between(start_date='-2y', end_date='today').strftime('%d-%m-%Y')
        historico = fake.text(max_nb_chars=300).replace("'", "''")
        insert = f"INSERT INTO PRONTUARIO (id_paciente, data_criacao, historico) VALUES ({id_paciente}, TO_DATE('{data_criacao}', 'DD-MM-YYYY'), '{historico}')"
        prontuario_inserts.append(insert)
    return prontuario_inserts
def gerar_atestado():
    # 11 - ATESTADO
    atestado_inserts = []
    for i in range(QTD):

        id_prontuario = i + 1
        precisa_atestado = random.random() <0.50

        if precisa_atestado:
            data_emissao = fake.date_between(start_date='-1y', end_date='today').strftime('%d-%m-%Y')
            motivo = fake.sentence(nb_words=12).replace("'", "''")
            dias_afast = random.randint(1, 30)
            insert = f"INSERT INTO ATESTADO (id_prontuario, data_emissao, motivo, dias_afastamento) VALUES ({id_prontuario}, TO_DATE('{data_emissao}', 'DD-MM-YYYY'), '{motivo}', {dias_afast})"
            atestado_inserts.append(insert)
    return atestado_inserts


lista_gerar = [gerar_pessoas(),gerar_departamento(),gerar_funcionario(),gerar_especialidades(),gerar_medico(),
                  gerar_convenio(),gerar_paciente(),gerar_consultas(),gerar_formulario(),gerar_prontuario(),gerar_atestado()]


def select_pessoas():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    tabelas = []
    sql = f"select * from {tabelas}"
    cursor.execute(sql)
    colunas = [desc[0] for desc in cursor.description]
    print(colunas)
    resultado = cursor.fetchall()
    for linha   in resultado:
        print(linha)




def inserir_dados():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    try:
        funcoes_geradoras = [
            gerar_pessoas,
            gerar_departamento,
            gerar_funcionario,
            gerar_especialidades,
            gerar_medico,
            gerar_convenio,
            gerar_paciente,
            gerar_consultas,
            gerar_formulario,
            gerar_prontuario,
            gerar_atestado
        ]

        for func in funcoes_geradoras:
            lista = func()
            print(f"\n>>> Inserindo dados de: {func.__name__}")
            for insert in lista:
                try:
                    print("Executando:", repr(insert))
                    cursor.execute(insert)
                except Exception as e:
                    print(f"Erro ao executar insert: {e}\n{insert}")
                    conexao.rollback()
                    return  # Encerra ao primeiro erro

        conexao.commit()
        print("\nTodos os dados foram inseridos com sucesso!")

    except Exception as e:
        print(f"Erro geral: {e}")
        conexao.rollback()

    finally:
        cursor.close()
        conexao.close()



