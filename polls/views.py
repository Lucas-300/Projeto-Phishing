from django.shortcuts import render
import pandas as pd
from joblib import load
import os

# Caminho do modelo
MODEL_PATH = 'polls/PhishingModel.joblib'

# Carregando o modelo na inicialização do servidor
try:
    loaded_model = load(MODEL_PATH)
    print("Modelo carregado com sucesso!")
except Exception as e:
    print(f"Erro ao carregar o modelo: {e}")

def index_func(request):
    prediction = None  # Inicializando a variável de predição

    if request.method == 'POST':
        # Obtendo os dados do formulário
        url = request.POST.get('url', '')
        num_dots = request.POST.get('NumDots', '')
        path_level = request.POST.get('PathLevel', '')
        num_dash = request.POST.get('NumDash', '')
        num_sensitive_words = request.POST.get('NumSensitiveWords', '')
        pct_ext_hyperlinks = request.POST.get('PctExtHyperlinks', '')
        pct_ext_resource_urls = request.POST.get('PctExtResourceUrls', '')
        insecure_forms = request.POST.get('InsecureForms', '')
        pct_null_self_redirect_hyperlinks = request.POST.get('PctNullSelfRedirectHyperlinks', '')
        frequent_domain_name_mismatch = request.POST.get('FrequentDomainNameMismatch', '')
        submit_info_to_email = request.POST.get('SubmitInfoToEmail', '')
        iframe_or_frame = request.POST.get('IframeOrFrame', '')  # Novo campo

        try:
            # Convertendo valores para float ou atribuindo um padrão caso estejam vazios
            num_dots = float(num_dots) if num_dots else 0.0
            path_level = float(path_level) if path_level else 0.0
            num_dash = float(num_dash) if num_dash else 0.0
            num_sensitive_words = float(num_sensitive_words) if num_sensitive_words else 0.0
            pct_ext_hyperlinks = float(pct_ext_hyperlinks) if pct_ext_hyperlinks else 0.0
            pct_ext_resource_urls = float(pct_ext_resource_urls) if pct_ext_resource_urls else 0.0

            # Tratando campos de "Sim" ou "Não" para valores binários
            insecure_forms = 1 if insecure_forms.strip().lower() == 'sim' else 0
            submit_info_to_email = 1 if submit_info_to_email.strip().lower() == 'sim' else 0
            iframe_or_frame = 1 if iframe_or_frame.strip().lower() == 'sim' else 0  # Convertendo para 1 ou 0

            pct_null_self_redirect_hyperlinks = float(pct_null_self_redirect_hyperlinks) if pct_null_self_redirect_hyperlinks else 0.0
            frequent_domain_name_mismatch = int(frequent_domain_name_mismatch) if frequent_domain_name_mismatch else 0

            # Criando o DataFrame para predição
            input_data = pd.DataFrame([{
                'NumDots': num_dots,
                'PathLevel': path_level,
                'NumDash': num_dash,
                'NumSensitiveWords': num_sensitive_words,
                'PctExtHyperlinks': pct_ext_hyperlinks,
                'PctExtResourceUrls': pct_ext_resource_urls,
                'InsecureForms': insecure_forms,
                'PctNullSelfRedirectHyperlinks': pct_null_self_redirect_hyperlinks,
                'FrequentDomainNameMismatch': frequent_domain_name_mismatch,
                'SubmitInfoToEmail': submit_info_to_email,
                'IframeOrFrame': iframe_or_frame,  # Adicionando o campo IframeOrFrame
            }])

            # Realizando a predição com o modelo carregado
            prediction_result = loaded_model.predict(input_data)
            prediction = "É um site de phishing!" if prediction_result[0] == 1 else "Não é um site de phishing."

        except ValueError as e:
            # Caso valores inválidos sejam enviados
            print(f"Erro de valor: {e}")
            return render(request, "index.html", {'prediction': f"Erro de entrada: {e}"})
        except Exception as e:
            # Tratando erros no modelo
            print(f"Erro ao processar a predição: {e}")
            return render(request, "index.html", {'prediction': f"Erro ao processar a predição: {e}"})

    return render(request, "index.html", {'prediction': prediction})

def funcionalidades(request):
    try:
        return render(request, 'funcionalidades.html')
    except Exception as e:
        print(f"Erro ao renderizar funcionalidades: {e}")
        return render(request, "index.html", {'prediction': f"Erro ao carregar a página de funcionalidades: {e}"})
