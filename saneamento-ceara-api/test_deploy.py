#!/usr/bin/env python3
"""
Script de teste para verificar a configuração de deploy
"""

import os
import sys
import subprocess
from pathlib import Path

def check_file_exists(file_path, description):
    """Verifica se um arquivo existe"""
    if Path(file_path).exists():
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} - NÃO ENCONTRADO")
        return False

def check_requirements():
    """Verifica se os requirements estão corretos"""
    print("\n📦 Verificando requirements.txt...")
    
    required_packages = [
        "fastapi",
        "uvicorn[standard]",
        "sqlalchemy",
        "psycopg2-binary",
        "gunicorn"
    ]
    
    try:
        with open("requirements.txt", "r") as f:
            content = f.read()
            
        missing_packages = []
        for package in required_packages:
            if package not in content:
                missing_packages.append(package)
        
        if missing_packages:
            print(f"❌ Pacotes faltando: {', '.join(missing_packages)}")
            return False
        else:
            print("✅ Todos os pacotes necessários estão presentes")
            return True
    except FileNotFoundError:
        print("❌ requirements.txt não encontrado")
        return False

def check_docker():
    """Verifica se o Dockerfile está correto"""
    print("\n🐳 Verificando Dockerfile...")
    
    try:
        with open("Dockerfile", "r") as f:
            content = f.read()
        
        required_commands = [
            "FROM python:3.10-slim",
            "COPY requirements.txt",
            "RUN pip install",
            "EXPOSE 8000",
            "CMD"
        ]
        
        missing_commands = []
        for command in required_commands:
            if command not in content:
                missing_commands.append(command)
        
        if missing_commands:
            print(f"❌ Comandos faltando no Dockerfile: {', '.join(missing_commands)}")
            return False
        else:
            print("✅ Dockerfile parece estar correto")
            return True
    except FileNotFoundError:
        print("❌ Dockerfile não encontrado")
        return False

def check_environment_variables():
    """Verifica variáveis de ambiente necessárias"""
    print("\n🔧 Verificando variáveis de ambiente...")
    
    required_vars = ["DATABASE_URL", "ENVIRONMENT", "PORT"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️  Variáveis de ambiente não definidas: {', '.join(missing_vars)}")
        print("   (Isso é normal em desenvolvimento local)")
        return True
    else:
        print("✅ Todas as variáveis de ambiente estão definidas")
        return True

def check_app_structure():
    """Verifica a estrutura da aplicação"""
    print("\n📁 Verificando estrutura da aplicação...")
    
    required_files = [
        "app/main.py",
        "app/database.py",
        "app/models.py",
        "app/routers/",
        "alembic.ini"
    ]
    
    all_exist = True
    for file_path in required_files:
        if not check_file_exists(file_path, f"Arquivo/Diretório"):
            all_exist = False
    
    return all_exist

def main():
    """Função principal"""
    print("🚀 Verificando configuração para deploy no Cloud Render")
    print("=" * 60)
    
    # Verificar arquivos de deploy
    print("\n📋 Verificando arquivos de deploy...")
    deploy_files = [
        ("render.yaml", "Configuração do Cloud Render"),
        ("Dockerfile", "Configuração do Docker"),
        ("gunicorn.conf.py", "Configuração do Gunicorn"),
        ("start.sh", "Script de inicialização"),
        ("Procfile", "Configuração do Procfile"),
        ("runtime.txt", "Versão do Python"),
        (".dockerignore", "Arquivos ignorados pelo Docker")
    ]
    
    deploy_files_ok = True
    for file_path, description in deploy_files:
        if not check_file_exists(file_path, description):
            deploy_files_ok = False
    
    # Verificar requirements
    requirements_ok = check_requirements()
    
    # Verificar Dockerfile
    docker_ok = check_docker()
    
    # Verificar estrutura da aplicação
    app_structure_ok = check_app_structure()
    
    # Verificar variáveis de ambiente
    env_ok = check_environment_variables()
    
    # Resumo
    print("\n" + "=" * 60)
    print("📊 RESUMO DA VERIFICAÇÃO")
    print("=" * 60)
    
    checks = [
        ("Arquivos de Deploy", deploy_files_ok),
        ("Requirements", requirements_ok),
        ("Dockerfile", docker_ok),
        ("Estrutura da Aplicação", app_structure_ok),
        ("Variáveis de Ambiente", env_ok)
    ]
    
    all_passed = True
    for check_name, passed in checks:
        status = "✅ PASSOU" if passed else "❌ FALHOU"
        print(f"{check_name}: {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ O projeto está pronto para deploy no Cloud Render")
        print("\n📝 Próximos passos:")
        print("1. Faça commit de todas as alterações")
        print("2. Push para o repositório Git")
        print("3. Acesse o Cloud Render Dashboard")
        print("4. Crie um novo Blueprint ou Web Service")
        print("5. Conecte seu repositório")
        print("6. Configure as variáveis de ambiente")
        print("7. Deploy!")
    else:
        print("⚠️  ALGUNS TESTES FALHARAM")
        print("❌ Corrija os problemas antes do deploy")
        print("\n📝 Verifique:")
        print("- Arquivos faltando")
        print("- Dependências incorretas")
        print("- Configurações inválidas")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main()) 