#!/usr/bin/env python3
"""
Script de gerenciamento para a API de Saneamento do Ceará
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

# Adicionar o diretório raiz ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def run_command(command, description):
    """Executa um comando e exibe o resultado"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} concluído com sucesso!")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao {description.lower()}:")
        print(f"Comando: {command}")
        print(f"Erro: {e.stderr}")
        return False

def check_docker():
    """Verifica se o Docker está rodando"""
    try:
        subprocess.run(["docker", "info"], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def start_database():
    """Inicia o banco de dados PostgreSQL via Docker"""
    if not check_docker():
        print("❌ Docker não está disponível. Instale o Docker primeiro.")
        return False
    
    print("🐳 Iniciando banco de dados PostgreSQL...")
    return run_command(
        "docker-compose up -d db",
        "Iniciar banco de dados"
    )

def stop_database():
    """Para o banco de dados"""
    if not check_docker():
        print("❌ Docker não está disponível.")
        return False
    
    print("🛑 Parando banco de dados...")
    return run_command(
        "docker-compose down",
        "Parar banco de dados"
    )

def run_migrations():
    """Executa as migrações do banco de dados"""
    print("📊 Executando migrações...")
    
    # Verificar se o ambiente virtual existe
    venv_path = project_root / "venv"
    if not venv_path.exists():
        print("❌ Ambiente virtual não encontrado. Execute 'python3 -m venv venv' primeiro.")
        return False
    
    # Ativar ambiente virtual e executar migrações
    activate_script = venv_path / "bin" / "activate"
    if os.name == 'nt':  # Windows
        activate_script = venv_path / "Scripts" / "activate.bat"
    
    command = f"source {activate_script} && alembic upgrade head"
    if os.name == 'nt':
        command = f"{activate_script} && alembic upgrade head"
    
    return run_command(command, "Executar migrações")

def start_api():
    """Inicia a API"""
    print("🚀 Iniciando API...")
    
    # Verificar se o ambiente virtual existe
    venv_path = project_root / "venv"
    if not venv_path.exists():
        print("❌ Ambiente virtual não encontrado. Execute 'python3 -m venv venv' primeiro.")
        return False
    
    # Ativar ambiente virtual e iniciar API
    activate_script = venv_path / "bin" / "activate"
    if os.name == 'nt':  # Windows
        activate_script = venv_path / "Scripts" / "activate.bat"
    
    command = f"source {activate_script} && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
    if os.name == 'nt':
        command = f"{activate_script} && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
    
    print("🔄 Iniciando servidor...")
    try:
        subprocess.run(command, shell=True, check=True)
    except KeyboardInterrupt:
        print("\n🛑 API interrompida pelo usuário.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao iniciar API: {e}")
        return False
    
    return True

def install_dependencies():
    """Instala as dependências do projeto"""
    print("📦 Instalando dependências...")
    
    # Verificar se o ambiente virtual existe
    venv_path = project_root / "venv"
    if not venv_path.exists():
        print("❌ Ambiente virtual não encontrado. Criando...")
        if not run_command("python3 -m venv venv", "Criar ambiente virtual"):
            return False
    
    # Ativar ambiente virtual e instalar dependências
    activate_script = venv_path / "bin" / "activate"
    if os.name == 'nt':  # Windows
        activate_script = venv_path / "Scripts" / "activate.bat"
    
    command = f"source {activate_script} && pip install -r requirements.txt"
    if os.name == 'nt':
        command = f"{activate_script} && pip install -r requirements.txt"
    
    return run_command(command, "Instalar dependências")

def check_health():
    """Verifica a saúde da API"""
    print("🏥 Verificando saúde da API...")
    
    try:
        import requests
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ API está funcionando corretamente!")
            print(f"Resposta: {response.json()}")
            return True
        else:
            print(f"❌ API retornou status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Não foi possível conectar à API: {e}")
        return False

def show_logs():
    """Exibe os logs da aplicação"""
    log_file = project_root / "logs" / "api.log"
    if not log_file.exists():
        print("❌ Arquivo de log não encontrado.")
        return False
    
    print("📋 Últimas 20 linhas do log:")
    try:
        with open(log_file, 'r') as f:
            lines = f.readlines()
            for line in lines[-20:]:
                print(line.rstrip())
        return True
    except Exception as e:
        print(f"❌ Erro ao ler logs: {e}")
        return False

def setup_project():
    """Configura o projeto completo"""
    print("🔧 Configurando projeto completo...")
    
    steps = [
        ("Instalar dependências", install_dependencies),
        ("Iniciar banco de dados", start_database),
        ("Executar migrações", run_migrations),
    ]
    
    for step_name, step_func in steps:
        print(f"\n--- {step_name} ---")
        if not step_func():
            print(f"❌ Falha em: {step_name}")
            return False
    
    print("\n✅ Projeto configurado com sucesso!")
    print("🚀 Para iniciar a API, execute: python scripts/manage.py start")
    return True

def main():
    parser = argparse.ArgumentParser(description="Gerenciador da API de Saneamento do Ceará")
    parser.add_argument("command", choices=[
        "setup", "start", "stop", "migrate", "health", "logs", "db-start", "db-stop"
    ], help="Comando a executar")
    
    args = parser.parse_args()
    
    # Mudar para o diretório do projeto
    os.chdir(project_root)
    
    if args.command == "setup":
        setup_project()
    elif args.command == "start":
        start_api()
    elif args.command == "stop":
        stop_database()
    elif args.command == "migrate":
        run_migrations()
    elif args.command == "health":
        check_health()
    elif args.command == "logs":
        show_logs()
    elif args.command == "db-start":
        start_database()
    elif args.command == "db-stop":
        stop_database()

if __name__ == "__main__":
    main() 