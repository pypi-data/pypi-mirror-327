# ==============================
# 1) Manipulação de Dados
# ==============================
import numpy as np
import pandas as pd
import itertools
from itertools import combinations

# ==============================
# 2) Formatação e Exibição de Tabelas
# ==============================
from tabulate import tabulate

# ==============================
# 3) Modelos Estatísticos (Regressão, GLM)
# ==============================
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.formula.api import glm
from statsmodels.miscmodels.ordinal_model import OrderedModel

# ==============================
# 4) Análise Estatística (Distribuições, Testes de Hipótese)
# ==============================
from scipy import stats
from scipy.stats import norm, chi2

# ==============================
# 5) Métricas de Avaliação de Modelos
# ==============================
from sklearn.metrics import (
    confusion_matrix, accuracy_score, precision_score, recall_score, 
    f1_score, roc_curve, roc_auc_score, auc
)

# ==============================
# 6) Visualização Interativa (Plotly)
# ==============================
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.colors import qualitative

# ==============================
# 7) Visualização com Matplotlib
# ==============================
import matplotlib.pyplot as plt


import numpy as np
from itertools import combinations
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import plotly.graph_objects as go
import pandas as pd
from plotly.colors import qualitative

import warnings
warnings.filterwarnings("ignore", message="overflow encountered in exp")
warnings.filterwarnings("ignore", message="divide by zero encountered in log")
warnings.filterwarnings("ignore", message="Inverting hessian failed, no bse or cov_params available")



def analyze_glm_binomial(df, dependent_var, independent_vars):
    """
    Ajusta um modelo GLM binomial (logístico) a partir de um DataFrame, exibindo medidas de ajuste,
    testes do modelo e estimativas dos parâmetros.

    Parâmetros:
    - df: DataFrame com dados
    - dependent_var: Nome da variável dependente (binária, 0/1)
    - independent_vars: Lista de nomes de variáveis independentes

    A função valida a existência das variáveis, ajusta o modelo completo,
    realiza testes (Omnibus, LR de efeito), gera tabelas de ajuste e estimativas.
    """

    # Validação das variáveis
    all_vars = [dependent_var] + independent_vars
    for var in all_vars:
        if var not in df.columns:
            raise ValueError(f"A variável '{var}' não existe no DataFrame.")

    # Agrupar os dados pelas variáveis independentes e contar sucessos e fracassos
    grouped = df.groupby(independent_vars)[dependent_var].agg(['sum', 'count']).reset_index()
    grouped.columns = independent_vars + ['Success', 'Total']
    grouped['Failure'] = grouped['Total'] - grouped['Success']

    n_groups = len(grouped)
    n_total = df.shape[0]

    # Preparar as matrizes de design
    X_full = grouped[independent_vars]
    y = grouped[['Success', 'Failure']]
    X_full = sm.add_constant(X_full)

    # Ajustar o modelo completo
    model_full = sm.GLM(y, X_full, family=sm.families.Binomial())
    result_full = model_full.fit()
    deviance_full = result_full.deviance
    df_resid = result_full.df_resid
    df_model = result_full.df_model
    k = len(result_full.params)
    pearson_chi2 = np.sum(result_full.resid_pearson**2)
    log_likelihood_full = result_full.llf

    # Critérios de informação
    aic = -2 * log_likelihood_full + 2 * k
    bic = -2 * log_likelihood_full + k * np.log(n_total)
    AICc = aic + (2 * k * (k + 1)) / (n_total - k - 1)
    CAIC = aic + (np.log(n_total) + 1) * k

    # Estimação do parâmetro de escala (usando a deviance)
    scale = deviance_full / df_resid  # Método da Deviance

    # Ajuste dos erros padrão
    adjusted_bse = result_full.bse * np.sqrt(scale)

    # Recalcular Wald Chi-Quadrado e p-valores com os erros padrão ajustados
    wald_chi2 = (result_full.params / adjusted_bse) ** 2
    p_values = 1 - stats.chi2.cdf(wald_chi2, df=1)
    wald_chi2 = pd.Series(wald_chi2, index=result_full.params.index)
    p_values = pd.Series(p_values, index=result_full.params.index)

    # Testes tipo III (Likelihood Ratio) para cada parâmetro
    LR_stats = {}
    p_values_lr = {}
    for var in ['const'] + independent_vars:
        if var == 'const':
            # Modelo sem intercepto
            X_reduced = grouped[independent_vars]  # sem adicionar constante
        else:
            # Modelo sem a variável atual
            vars_reduced = [v for v in independent_vars if v != var]
            X_reduced = grouped[vars_reduced]
            X_reduced = sm.add_constant(X_reduced)

        model_reduced = sm.GLM(y, X_reduced, family=sm.families.Binomial())
        result_reduced = model_reduced.fit()
        deviance_reduced = result_reduced.deviance
        LR_stat = (deviance_reduced - deviance_full) / scale
        p_value_lr = 1 - stats.chi2.cdf(LR_stat, df=1)
        LR_stats[var] = LR_stat
        p_values_lr[var] = p_value_lr

    # Funções auxiliares de formatação
    def format_number(x):
        if isinstance(x, (int, float, np.float64, np.int64)):
            return f"{x:.3f}"
        else:
            return x

    def format_p_value(p):
        return "<0.001" if p < 0.001 else f"{p:.3f}"

    def create_goodness_of_fit_table():
        """
        Cria e exibe a tabela de "Goodness of Fit" com notas explicativas.
        """
        def add_superscript(text, superscripts):
            return f"{text}^{superscripts}"

        title = add_superscript('Goodness of Fit', 'a,b,c,d')
        log_likelihood_label = add_superscript('Log Likelihood', 'b,c')
        adjusted_log_likelihood_label = add_superscript('Adjusted Log Likelihood', 'd')

        # Usar escala fixa em 1 para Scaled Deviance (opcional)
        scale_fixed = 1
        scaled_deviance = df_resid * scale_fixed
        # Scaled Pearson: relação do Pearson Chi2 com a deviance
        scaled_pearson_chi2 = pearson_chi2 * (df_resid / deviance_full)

        adjusted_log_likelihood = -0.5 * scaled_deviance

        table = [
            ['Deviance', deviance_full, df_resid, deviance_full / df_resid],
            ['Scaled Deviance', scaled_deviance, df_resid, ''],
            ['Pearson Chi-Square', pearson_chi2, df_resid, pearson_chi2 / df_resid],
            ['Scaled Pearson Chi-Square', scaled_pearson_chi2, df_resid, ''],
            [log_likelihood_label, log_likelihood_full, '', ''],
            [adjusted_log_likelihood_label, adjusted_log_likelihood, '', ''],
            ["Akaike's Information Criterion (AIC)", aic, '', ''],
            ['Finite Sample Corrected AIC (AICc)', AICc, '', ''],
            ['Bayesian Information Criterion (BIC)', bic, '', ''],
            ['Consistent AIC (CAIC)', CAIC, '', '']
        ]
        headers = [title, 'Value', 'df', 'Value/df']

        formatted_table = []
        for row in table:
            formatted_row = [row[0]] + [format_number(x) for x in row[1:]]
            formatted_table.append(formatted_row)

        print(tabulate(formatted_table, headers=headers))

        footnotes = [
            "a. Information criteria are in smaller-is-better form.",
            "b. The full log likelihood function is displayed and used in computing information criteria.",
            "c. The log likelihood is based on a scale parameter fixed at 1.",
            "d. The adjusted log likelihood is based on the residual deviance and dispersion scaling."
        ]
        print('\n' + '\n'.join(footnotes))

    def create_omnibus_test_table():
        """
        Cria e exibe a tabela do teste Omnibus, comparando o modelo completo com o modelo nulo.
        """
        X_null = pd.DataFrame({'const': np.ones(grouped.shape[0])})
        model_null = sm.GLM(y, X_null, family=sm.families.Binomial())
        result_null = model_null.fit()
        deviance_null = result_null.deviance

        LR_stat_omnibus = (deviance_null - deviance_full) / scale
        p_value_omnibus = 1 - stats.chi2.cdf(LR_stat_omnibus, df=len(independent_vars))
        table = [
            [format_number(LR_stat_omnibus), len(independent_vars), format_p_value(p_value_omnibus)]
        ]
        headers = ['Likelihood Ratio Chi-Square', 'df', 'Sig.']
        print("Omnibus Tests of Model Coefficients")
        print(tabulate(table, headers=headers))

        footnotes = [
            "a. Compares the fitted model against the intercept-only model.",
            f"Dependent Variable: {dependent_var}",
            f"Model: (Intercept), {', '.join(independent_vars)}"
        ]
        print('\n' + '\n'.join(footnotes))

    def create_test_of_model_effects_table():
        """
        Cria e exibe a tabela com Testes Tipo III de Efeitos do Modelo (LR Tests).
        """
        df1 = 1
        df2 = df_resid

        table = []
        for var in ['const'] + independent_vars:
            source_name = '(Intercept)' if var == 'const' else var
            row = [
                source_name,
                format_number(LR_stats[var]),
                df1,
                format_p_value(p_values_lr[var]),
                format_number(LR_stats[var]),
                df1,
                format_number(df2),
                format_p_value(p_values_lr[var])
            ]
            table.append(row)

        headers = ['Source', 'Type III LR Chi-Square', 'df', 'Sig.', 'F', 'df1', 'df2', 'Sig.']
        print("Tests of Model Effects")
        print(tabulate(table, headers=headers))

        footnotes = [
            f"Dependent Variable: {dependent_var}",
            f"Model: (Intercept), {', '.join(independent_vars)}"
        ]
        print('\n' + ', '.join(footnotes))

    def create_parameter_estimates_table():
        """
        Cria e exibe a tabela de estimativas dos parâmetros, incluindo intervalos de confiança,
        razão de chances (Exp(B)) e testes de significância.
        """
        conf_int = result_full.conf_int()
        conf_int.columns = ['Lower', 'Upper']
        # Ajuste dos intervalos com os erros padrão escalonados
        conf_int['Lower'] = result_full.params - stats.norm.ppf(0.975) * adjusted_bse
        conf_int['Upper'] = result_full.params + stats.norm.ppf(0.975) * adjusted_bse

        exp_coef = np.exp(result_full.params)
        exp_conf_int_lower = np.exp(conf_int['Lower'])
        exp_conf_int_upper = np.exp(conf_int['Upper'])

        table = []
        for i in range(len(result_full.params)):
            param_name = result_full.params.index[i]
            row = [
                param_name if param_name != 'const' else '(Intercept)',
                format_number(result_full.params.iloc[i]),
                format_number(adjusted_bse.iloc[i]),
                format_number(conf_int.iloc[i]['Lower']),
                format_number(conf_int.iloc[i]['Upper']),
                format_number(wald_chi2[param_name]),
                1,
                format_p_value(p_values[param_name]),
                format_number(exp_coef.iloc[i]),
                format_number(exp_conf_int_lower.iloc[i]),
                format_number(exp_conf_int_upper.iloc[i])
            ]
            table.append(row)

        # Adicionar linha do parâmetro de escala
        table.append([
            '(Scale)',
            format_number(scale),
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            ''
        ])

        headers = [
            'Parameter', 'B', 'Std. Error',
            'Lower', 'Upper',
            'Wald Chi-Square', 'df', 'Sig.',
            'Exp(B)', 'Lower', 'Upper'
        ]
        print("Parameter Estimates (Adjusted for Deviance)")
        print(tabulate(table, headers=headers))

        footnotes = [
            f"Dependent Variable: {dependent_var}",
            f"Model: (Intercept), {', '.join(independent_vars)}",
            "a. Scale parameter estimated using the deviance."
        ]
        print('\n' + '\n'.join(footnotes))

    # Exibir resultados
    print(f"Número de observações: {n_total}")
    print(f"Número de grupos (combinações únicas): {n_groups}\n")
    create_goodness_of_fit_table()
    print()
    create_omnibus_test_table()
    print()
    create_test_of_model_effects_table()
    print()
    create_parameter_estimates_table()


def analyze_glm_binomial_plots(df, dependent_var, independent_vars):
    """
    Ajusta um modelo GLM binomial (logístico) e plota:
    - logit(p) versus a variável independente
    - Probabilidade prevista versus a variável independente

    Parâmetros:
    - df: DataFrame com dados
    - dependent_var: Nome da variável dependente (binária)
    - independent_vars: Lista de variáveis independentes (assume apenas uma, neste exemplo)

    Retorno:
    - Figura plotly com dois subplots.
    """

    # Validação
    all_vars = [dependent_var] + independent_vars
    for var in all_vars:
        if var not in df.columns:
            raise ValueError(f"A variável '{var}' não existe no DataFrame.")

    # Agrupar e montar o modelo
    grouped = df.groupby(independent_vars)[dependent_var].agg(['sum', 'count']).reset_index()
    grouped.columns = independent_vars + ['Success', 'Total']
    grouped['Failure'] = grouped['Total'] - grouped['Success']

    X_full = grouped[independent_vars]
    y = grouped[['Success', 'Failure']]
    X_full = sm.add_constant(X_full)

    model = sm.GLM(y, X_full, family=sm.families.Binomial())
    result = model.fit()

    intercept = result.params['const']
    coef = result.params[independent_vars[0]]
    equation = f"logit(p) = {intercept:.3f} + {coef:.5f} * {independent_vars[0]}"

    # Criar uma cópia explícita do DataFrame para evitar SettingWithCopyWarning
    df_copy = df.copy()

    # Adicionar colunas previstas ao DataFrame
    df_copy.loc[:, 'predicted_prob'] = result.predict(sm.add_constant(df_copy[independent_vars]))
    df_copy.loc[:, 'logit_p'] = np.log(df_copy['predicted_prob'] / (1 - df_copy['predicted_prob']))
    df_sorted = df_copy.sort_values(by=independent_vars[0])

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=(f"Logit(p) vs {independent_vars[0]}", f"Predicted Probability vs {independent_vars[0]}")
    )

    # Logit(p)
    fig.add_trace(go.Scatter(
        x=df_sorted[independent_vars[0]],
        y=coef * df_sorted[independent_vars[0]] + intercept,
        mode='lines', name='Logit Regression Line', line=dict(color='orange')
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=df_sorted[independent_vars[0]],
        y=df_sorted['logit_p'], mode='markers', name='logit(p)',
        marker=dict(color='red', size=3)
    ), row=1, col=1)
    
    # Probabilidade prevista
    fig.add_trace(go.Scatter(
        x=df_sorted[independent_vars[0]],
        y=df_sorted['predicted_prob'], mode='lines', name='Predicted Probability',
        line=dict(color='lightblue')
    ), row=1, col=2)

    fig.add_trace(go.Scatter(
        x=df_sorted[independent_vars[0]],
        y=df_sorted['predicted_prob'], mode='markers', name='Highlighted Points',
        marker=dict(color='blue', size=3)
    ), row=1, col=2)

    fig.update_layout(
        title_text="Logistic Regression Analysis (GLM Binomial)",
        width=1200,
        height=600,
        annotations=[
            dict(
                x=0.25,
                y=1.05,
                showarrow=False,
                text=equation,
                xref="paper",
                yref="paper",
                font=dict(size=12),
            )
        ],
        xaxis1_title=independent_vars[0],
        yaxis1_title="logit(p)",
        xaxis2_title=independent_vars[0],
        yaxis2_title="Predicted Probability",
    )

    fig.show()
    
    return df_copy


def classification_table(df, actual_col, predicted_prob_col, threshold=0.5):
    """
    Gera uma tabela de classificação a partir de um threshold para as probabilidades preditas.

    Parâmetros:
    - df: DataFrame com dados
    - actual_col: Nome da coluna com valores observados (0 ou 1)
    - predicted_prob_col: Nome da coluna com probabilidades previstas
    - threshold: ponto de corte

    Retorna:
    - Exibe a tabela de classificação formatada.
    """
    df = df.copy()
    df['predicted_class'] = np.where(df[predicted_prob_col] >= threshold, 1, 0)
    
    tn, fp, fn, tp = confusion_matrix(df[actual_col], df['predicted_class']).ravel()
    
    total = tn + fp + fn + tp
    total_nao = tn + fp
    total_sim = fn + tp
    total_previsto_nao = tn + fn
    total_previsto_sim = fp + tp

    especificidade = (tn / total_nao * 100) if total_nao != 0 else 0
    sensibilidade = (tp / total_sim * 100) if total_sim != 0 else 0
    precisao = (tp / total_previsto_sim * 100) if total_previsto_sim != 0 else 0

    table = [
        ["Real\\Previsão", "Previsto Não (0)", "Previsto Sim (1)", "Total"],
        ["Real Não (0)", tn, fp, total_nao],
        ["Real Sim (1)", fn, tp, total_sim],
        ["Total", total_previsto_nao, total_previsto_sim, total],
        ["", "", "", ""],
        ["Especificidade", f"{especificidade:.2f}%", ""],
        ["Sensibilidade", f"{sensibilidade:.2f}%", ""],
        ["Precisão", f"{precisao:.2f}%", ""],
    ]
    
    print(tabulate(table, headers="firstrow", tablefmt="grid"))


def auc_roc_table_OLD(df, actual_col, predicted_prob_col):
    """
    Gera uma tabela da AUC da curva ROC com IC 95%.

    Parâmetros:
    - df: DataFrame com dados
    - actual_col: Nome da coluna com valores observados (0 ou 1)
    - predicted_prob_col: Nome da coluna com probabilidades previstas

    Retorna:
    - Exibe a tabela formatada da AUC.
    """
    df = df.copy()
    auc_value = roc_auc_score(df[actual_col], df[predicted_prob_col])

    n1 = np.sum(df[actual_col] == 1)
    n2 = np.sum(df[actual_col] == 0)
    if n1 == 0 or n2 == 0:
        raise ValueError("Classes positivas e negativas não podem estar vazias.")

    # Fórmulas de Hanley & McNeil (1982)
    Q1 = auc_value / (2 - auc_value)
    Q2 = (2 * auc_value**2) / (1 + auc_value)
    auc_se = np.sqrt((auc_value * (1 - auc_value) + (n1 - 1)*(Q1 - auc_value**2) + (n2 - 1)*(Q2 - auc_value**2)) / (n1*n2))
    
    z = 1.96
    lower_bound = max(0, auc_value - z * auc_se)
    upper_bound = min(1, auc_value + z * auc_se)

    z_value = (auc_value - 0.5) / auc_se
    p_value = 2 * (1 - norm.cdf(abs(z_value)))

    table = [
        ["Área (AUC)", "Erro Padrão", "95% IC Inferior", "95% IC Superior", "Significância"],
        [f"{auc_value:.3f}", f"{auc_se:.4f}", f"{lower_bound:.3f}", f"{upper_bound:.3f}", f"{p_value:.3f}"]
    ]

    print(tabulate(table, headers="firstrow", tablefmt="grid"))
    print("a. Sob a suposição não-paramétrica\nb. Hipótese nula: área verdadeira = 0.5")


def plot_odds_ratio_increments(
    df,
    modelo_final,
    dependent_var,
    independent_numerical_vars=[],
    independent_categorical_vars=[],
    increment_steps=10,
    max_increment=100
):
    """
    Plota o efeito (em termos de Odds Ratio) de variações nas variáveis independentes sobre a variável dependente.
    
    Para variáveis numéricas:
      - Se o modelo for binomial, os dados são agrupados e o modelo é reestimado (como na função original)
        para obter um coeficiente que faça sentido na interpretação (por exemplo, OR de 1.159 para incremento 10).
      - Se o modelo for multinomial/ordinal, usa-se o(s) coeficiente(s) do modelo final.
    
    Para variáveis categóricas:
      - Utiliza-se a codificação dummy (assumindo que o modelo use a notação "C(var)[T<level>]") para calcular o OR.
    
    Parâmetros
    ----------
    df : pd.DataFrame
        DataFrame com os dados.
    modelo_final : objeto statsmodels já ajustado
        Pode ser um modelo binomial (com params do tipo Series) ou multinomial/ordinal (params do tipo DataFrame).
    dependent_var : str
        Nome da variável dependente.
    independent_numerical_vars : list de str
        Lista com os nomes das variáveis numéricas.
    independent_categorical_vars : list de str
        Lista com os nomes das variáveis categóricas.
    increment_steps : float
        Passo dos incrementos (para variáveis numéricas).
    max_increment : float
        Incremento máximo a ser considerado (para variáveis numéricas).
    """
    
    # Obter os parâmetros do modelo e identificar o tipo
    model_params = modelo_final.params
    is_binomial = isinstance(model_params, pd.Series)
    is_multinomial = isinstance(model_params, pd.DataFrame)
    
    ##############################
    # Variáveis Numéricas
    ##############################
    for var in independent_numerical_vars:
        if var not in df.columns:
            raise ValueError(f"A variável '{var}' não existe no DataFrame.")
        
        increments = np.arange(0, max_increment + increment_steps, increment_steps)
        
        # Se o modelo for binomial, reagrupar os dados e reestimar o GLM para obter um coeficiente adequado
        if is_binomial:
            # Agrupar os dados pela variável e calcular sucessos e total
            grouped = df.groupby(var)[dependent_var].agg(['sum', 'count']).reset_index()
            grouped.columns = [var, 'Success', 'Total']
            grouped['Failure'] = grouped['Total'] - grouped['Success']
            
            # Preparar os dados e ajustar o GLM
            X = grouped[[var]]
            y = grouped[['Success', 'Failure']]
            X = sm.add_constant(X)
            model = sm.GLM(y, X, family=sm.families.Binomial())
            result = model.fit()
            
            if var not in result.params.index:
                print(f"[AVISO] Variável '{var}' não encontrada nos parâmetros do modelo reestimado.")
                continue
                
            coef = result.params[var]
            
            # Calcular OR para os incrementos
            or_values = np.exp(coef * increments)
            
            # Plot e tabela
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=increments, y=or_values,
                mode='lines+markers', name='OR'
            ))
            fig.update_layout(
                title=f"Efeito da variação em '{var}' sobre o OR (Binomial - dados agrupados)",
                xaxis_title=f"Incrementos em {var} (u.m.)",
                yaxis_title="Odds Ratio (OR)",
                width=800, height=500
            )
            fig.show()
            
            table = [
                [round(inc, 3), round(or_val, 3), f"{round((or_val - 1)*100, 1)}%"]
                for inc, or_val in zip(increments, or_values)
            ]
            print(tabulate(
                table,
                headers=[f"Incrementos em {var} (u.m.)", "Odds Ratio (OR)", "Acréscimo (%)"],
                tablefmt="grid"
            ))
        
        # Se o modelo for multinomial ou ordinal, usamos os coeficientes disponíveis para cada outcome
        elif is_multinomial:
            fig = go.Figure()
            table_data = {}
            for outcome in model_params.columns:
                if var not in model_params.index:
                    print(f"[AVISO] Variável '{var}' não encontrada nos parâmetros para outcome '{outcome}'.")
                    continue
                coef = model_params.loc[var, outcome]
                or_values = np.exp(coef * increments)
                fig.add_trace(go.Scatter(
                    x=increments, y=or_values,
                    mode='lines+markers', name=f"Outcome: {outcome}"
                ))
                table_data[outcome] = [
                    [round(inc, 3), round(or_val, 3), f"{round((or_val - 1)*100, 1)}%"]
                    for inc, or_val in zip(increments, or_values)
                ]
            fig.update_layout(
                title=f"Efeito da variação em '{var}' sobre o OR (Multinomial/Ordinal)",
                xaxis_title=f"Incrementos em {var} (u.m.)",
                yaxis_title="Odds Ratio (OR)",
                width=800, height=500
            )
            fig.show()
            for outcome, data in table_data.items():
                print(f"Outcome: {outcome}")
                print(tabulate(
                    data,
                    headers=[f"Incrementos em {var} (u.m.)", "Odds Ratio (OR)", "Acréscimo (%)"],
                    tablefmt="grid"
                ))
        else:
            # Fallback: se não for reconhecido, reagrupar (mesma lógica do binomial)
            grouped = df.groupby(var)[dependent_var].agg(['sum', 'count']).reset_index()
            grouped.columns = [var, 'Success', 'Total']
            grouped['Failure'] = grouped['Total'] - grouped['Success']
            X = grouped[[var]]
            y = grouped[['Success', 'Failure']]
            X = sm.add_constant(X)
            model = sm.GLM(y, X, family=sm.families.Binomial())
            result = model.fit()
            coef = result.params[var]
            or_values = np.exp(coef * increments)
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=increments, y=or_values,
                mode='lines+markers', name='OR'
            ))
            fig.update_layout(
                title=f"Efeito da variação em '{var}' sobre o OR",
                xaxis_title=f"Incrementos em {var} (u.m.)",
                yaxis_title="Odds Ratio (OR)",
                width=800, height=500
            )
            fig.show()
            table = [
                [round(inc, 3), round(or_val, 3), f"{round((or_val - 1)*100, 1)}%"]
                for inc, or_val in zip(increments, or_values)
            ]
            print(tabulate(
                table,
                headers=[f"Incrementos em {var} (u.m.)", "Odds Ratio (OR)", "Acréscimo (%)"],
                tablefmt="grid"
            ))
    
    ##############################
    # Variáveis Categóricas
    ##############################
    for var in independent_categorical_vars:
        if var not in df.columns:
            raise ValueError(f"A variável '{var}' não existe no DataFrame.")
        
        levels = sorted(df[var].unique())
        
        # Para modelos binomiais, assumindo que o modelo foi ajustado usando a codificação dummy (ex.: C(var))
        if is_binomial:
            # Procura parâmetros com a notação "C(var)[T.<level>]"
            dummy_params = [name for name in model_params.index if f"C({var})[T." in name]
            dummy_levels = [name.split("[T.")[1].split("]")[0] for name in dummy_params]
            # O nível de referência é aquele que não aparece entre os dummies
            baseline = None
            for lvl in levels:
                if str(lvl) not in dummy_levels:
                    baseline = lvl
                    break
            odds_dict = {}
            if baseline is not None:
                odds_dict[baseline] = 1.0
            for name in dummy_params:
                lvl = name.split("[T.")[1].split("]")[0]
                coef = model_params[name]
                odds_dict[lvl] = np.exp(coef)
            # Garantir que todos os níveis apareçam
            for lvl in levels:
                if lvl not in odds_dict:
                    odds_dict[lvl] = 1.0
            fig = go.Figure(data=[go.Bar(x=list(odds_dict.keys()), y=list(odds_dict.values()))])
            fig.update_layout(
                title=f"Efeito de '{var}' sobre o OR (Binomial)",
                xaxis_title=var,
                yaxis_title="Odds Ratio (OR)",
                width=800, height=500
            )
            fig.show()
        
        # Para modelos multinomiais/ordinais
        elif is_multinomial:
            outcomes = model_params.columns
            for outcome in outcomes:
                dummy_params = [name for name in model_params.index if f"C({var})[T." in name]
                odds_dict = {}
                dummy_levels = []
                for name in dummy_params:
                    coef = model_params.loc[name, outcome]
                    lvl = name.split("[T.")[1].split("]")[0]
                    dummy_levels.append(lvl)
                    odds_dict[lvl] = np.exp(coef)
                baseline = None
                for lvl in levels:
                    if str(lvl) not in dummy_levels:
                        baseline = lvl
                        break
                if baseline is not None:
                    odds_dict[baseline] = 1.0
                for lvl in levels:
                    if lvl not in odds_dict:
                        odds_dict[lvl] = 1.0
                fig = go.Figure(data=[go.Bar(x=list(odds_dict.keys()), y=list(odds_dict.values()))])
                fig.update_layout(
                    title=f"Efeito de '{var}' sobre o OR (Outcome: {outcome})",
                    xaxis_title=var,
                    yaxis_title="Odds Ratio (OR)",
                    width=800, height=500
                )
                fig.show()
        else:
            # Fallback semelhante ao binomial
            dummy_params = [name for name in model_params.index if f"C({var})[T." in name]
            dummy_levels = [name.split("[T.")[1].split("]")[0] for name in dummy_params]
            baseline = None
            for lvl in levels:
                if str(lvl) not in dummy_levels:
                    baseline = lvl
                    break
            odds_dict = {}
            if baseline is not None:
                odds_dict[baseline] = 1.0
            for name in dummy_params:
                lvl = name.split("[T.")[1].split("]")[0]
                coef = model_params[name]
                odds_dict[lvl] = np.exp(coef)
            for lvl in levels:
                if lvl not in odds_dict:
                    odds_dict[lvl] = 1.0
            fig = go.Figure(data=[go.Bar(x=list(odds_dict.keys()), y=list(odds_dict.values()))])
            fig.update_layout(
                title=f"Efeito de '{var}' sobre o OR",
                xaxis_title=var,
                yaxis_title="Odds Ratio (OR)",
                width=800, height=500
            )
            fig.show()



def calculate_independent_values_for_probabilities(df, dependent_var, independent_var, probabilities):
    """
    Dadas probabilidades desejadas, calcula quais valores da variável independente
    gerariam essas probabilidades no modelo logístico ajustado.

    Parâmetros:
    - df: DataFrame com dados
    - dependent_var: variável dependente (0/1)
    - independent_var: variável independente
    - probabilities: lista de probabilidades desejadas

    Retorna:
    - Exibe uma tabela com o valor do independente para cada p.
    """
    if dependent_var not in df.columns:
        raise ValueError(f"A variável dependente '{dependent_var}' não existe no DataFrame.")
    if independent_var not in df.columns:
        raise ValueError(f"A variável independente '{independent_var}' não existe no DataFrame.")

    grouped = df.groupby(independent_var)[dependent_var].agg(['sum', 'count']).reset_index()
    grouped.columns = [independent_var, 'Success', 'Total']
    grouped['Failure'] = grouped['Total'] - grouped['Success']

    X_full = grouped[[independent_var]]
    y = grouped[['Success', 'Failure']]
    X_full = sm.add_constant(X_full)

    model = sm.GLM(y, X_full, family=sm.families.Binomial())
    result = model.fit()

    intercept = result.params['const']
    coef = result.params[independent_var]

    def find_indep_value(p):
        return (np.log(p / (1 - p)) - intercept) / coef

    indep_values = [find_indep_value(p) for p in probabilities]

    table = [
        [f"{p:.3f}", f"{val:.3f}"] for p, val in zip(probabilities, indep_values)
    ]

    print(tabulate(
        table,
        headers=["Probabilidade (p)", f"Valor de {independent_var} (u.m.)"],
        tablefmt="grid"
    ))


def validate_logistic_model(df, dependent_var, independent_var, test_size=0.3, random_state=42):
    """
    Valida o modelo de regressão logística dividindo a amostra em treino e teste,
    estimando AUC na amostra de teste e exibindo uma tabela com IC e p-valor.

    Parâmetros:
    - df: DataFrame com dados
    - dependent_var: variável dependente (0/1)
    - independent_var: variável independente
    - test_size: proporção de teste (default=0.3)
    - random_state: semente para reprodutibilidade
    """
    if dependent_var not in df.columns:
        raise ValueError(f"A variável dependente '{dependent_var}' não existe no DataFrame.")
    if independent_var not in df.columns:
        raise ValueError(f"A variável independente '{independent_var}' não existe no DataFrame.")

    df = df.copy()
    np.random.seed(random_state)
    df['random'] = np.random.rand(len(df))

    train = df.loc[df['random'] > test_size].copy()
    test = df.loc[df['random'] <= test_size].copy()

    X_train = train[[independent_var]]
    y_train = train[dependent_var]
    X_train = sm.add_constant(X_train)

    X_test = test[[independent_var]]
    y_test = test[dependent_var]
    X_test = sm.add_constant(X_test)

    model = sm.Logit(y_train, X_train)
    result = model.fit(disp=False)

    test['Predicted_Prob'] = result.predict(X_test)

    auc = roc_auc_score(y_test, test['Predicted_Prob'])
    n1 = sum(y_test == 1)
    n2 = sum(y_test == 0)

    # Fórmula de Hanley & McNeil
    Q1 = auc / (2 - auc)
    Q2 = (2 * auc**2) / (1 + auc)
    auc_se = np.sqrt((auc * (1 - auc) + (n1 - 1)*(Q1 - auc**2) + (n2 - 1)*(Q2 - auc**2)) / (n1*n2))

    z = norm.ppf(0.975)
    lower_bound = auc - z * auc_se
    upper_bound = auc + z * auc_se
    if upper_bound > 1.0:
        upper_bound = 1.0

    z_score = (auc - 0.5) / auc_se
    p_value = 2 * (1 - norm.cdf(abs(z_score)))

    validation_table = [
        ["Área", f"{auc:.3f}", f"{auc_se:.3f}", f"{p_value:.3f}", f"{lower_bound:.3f}", f"{upper_bound:.3f}"]
    ]

    print(tabulate(
        validation_table,
        headers=["", "Area", "Std. Error", "Sig.", "Lower Bound (95%)", "Upper Bound (95%)"],
        tablefmt="grid",
        numalign="center"
    ))
    print("\na. Under the nonparametric assumption")
    print("b. Null hypothesis: true area = 0.5")

def validate_logistic_model_compare_auc(df, dependent_var, independent_var, test_size=0.3, random_state=42):
    """
    Ajusta um modelo de regressão logística, calcula AUC no treino e teste, IC 95%, 
    e compara a AUC de treino com a AUC de teste.
    """

    # Verificação de colunas
    if dependent_var not in df.columns:
        raise ValueError(f"A variável dependente '{dependent_var}' não existe no DataFrame.")
    if independent_var not in df.columns:
        raise ValueError(f"A variável independente '{independent_var}' não existe no DataFrame.")

    df = df.copy()
    np.random.seed(random_state)
    df['random'] = np.random.rand(len(df))

    train = df.loc[df['random'] > test_size].copy()
    test = df.loc[df['random'] <= test_size].copy()

    X_train = train[[independent_var]]
    y_train = train[dependent_var]
    X_train = sm.add_constant(X_train)

    X_test = test[[independent_var]]
    y_test = test[dependent_var]
    X_test = sm.add_constant(X_test)

    model = sm.Logit(y_train, X_train)
    result = model.fit(disp=False)

    train['Predicted_Prob'] = result.predict(X_train)
    test['Predicted_Prob'] = result.predict(X_test)

    def auc_confidence_interval(y_true, y_pred):
        auc_value = roc_auc_score(y_true, y_pred)
        n1 = np.sum(y_true == 1)
        n2 = np.sum(y_true == 0)
        Q1 = auc_value / (2 - auc_value)
        Q2 = (2 * auc_value**2) / (1 + auc_value)
        auc_se = np.sqrt((auc_value * (1 - auc_value) + (n1 - 1)*(Q1 - auc_value**2) + (n2 - 1)*(Q2 - auc_value**2)) / (n1*n2))
        z = norm.ppf(0.975)
        lower_bound = auc_value - z * auc_se
        upper_bound = auc_value + z * auc_se
        lower_bound = max(0, lower_bound)
        upper_bound = min(1, upper_bound)
        # Teste de hipótese (AUC != 0.5)
        z_score = (auc_value - 0.5) / auc_se
        p_value = 2 * (1 - norm.cdf(abs(z_score)))
        return auc_value, auc_se, p_value, lower_bound, upper_bound

    # Calcular AUC para treino e teste
    train_auc, train_auc_se, train_p_value, train_lower, train_upper = auc_confidence_interval(y_train, train['Predicted_Prob'])
    test_auc, test_auc_se, test_p_value, test_lower, test_upper = auc_confidence_interval(y_test, test['Predicted_Prob'])

    # Comparação direta das duas AUCs (assumindo independência entre as amostras)
    diff = train_auc - test_auc
    diff_se = np.sqrt(train_auc_se**2 + test_auc_se**2)
    z_diff = diff / diff_se
    p_diff = 2 * (1 - norm.cdf(abs(z_diff)))  # teste bicaudal se diff != 0

    validation_table = [
        ["Treino", f"{train_auc:.3f}", f"{train_auc_se:.3f}", f"{train_p_value:.3f}", f"{train_lower:.3f}", f"{train_upper:.3f}"],
        ["Teste", f"{test_auc:.3f}", f"{test_auc_se:.3f}", f"{test_p_value:.3f}", f"{test_lower:.3f}", f"{test_upper:.3f}"],
        ["Diferença (Treino - Teste)", f"{diff:.3f}", f"{diff_se:.3f}", f"{p_diff:.3f}", "-", "-"]
    ]

    # Observação: Para a diferença, não faz sentido IC usando o mesmo método direto, 
    # mas poderíamos apresentar um IC normal:
    # IC normal 95% da diferença:
    diff_lower = diff - norm.ppf(0.975)*diff_se
    diff_upper = diff + norm.ppf(0.975)*diff_se
    # Atualizar a linha da diferença com IC
    validation_table[-1][-2] = f"{diff_lower:.3f}"
    validation_table[-1][-1] = f"{diff_upper:.3f}"

    print(tabulate(
        validation_table,
        headers=["Amostra", "Área", "Std. Error", "Sig.", "Lower Bound (95%)", "Upper Bound (95%)"],
        tablefmt="grid",
        numalign="center"
    ))
    print("\na. Under the nonparametric assumption")
    print("b. Null hypothesis: true area = 0.5")
    print("c. For the difference: Null hypothesis: AUC_train = AUC_test")
    

def bootstrap_auc_difference(y_train, pred_train, y_test, pred_test, n_boot=1000, random_state=42):
    """
    Realiza um teste de bootstrap para a diferença entre AUCs de treino e teste.
    Retorna a diferença observada, o intervalo de confiança bootstrap e um p-valor aproximado.
    """
    np.random.seed(random_state)
    # Diferença observada
    observed_diff = roc_auc_score(y_train, pred_train) - roc_auc_score(y_test, pred_test)

    diffs = []
    n_train = len(y_train)
    n_test = len(y_test)

    # Reamostragem
    for _ in range(n_boot):
        # Amostra bootstrap para treino
        idx_train = np.random.choice(np.arange(n_train), size=n_train, replace=True)
        # Amostra bootstrap para teste
        idx_test = np.random.choice(np.arange(n_test), size=n_test, replace=True)

        y_train_boot = y_train[idx_train]
        pred_train_boot = pred_train[idx_train]

        y_test_boot = y_test[idx_test]
        pred_test_boot = pred_test[idx_test]

        auc_train_boot = roc_auc_score(y_train_boot, pred_train_boot)
        auc_test_boot = roc_auc_score(y_test_boot, pred_test_boot)

        diffs.append(auc_train_boot - auc_test_boot)

    diffs = np.array(diffs)
    # IC 95% pelo percentil
    lower_bound = np.percentile(diffs, 2.5)
    upper_bound = np.percentile(diffs, 97.5)

    # Cálculo do p-valor
    # p-valor bicaudal: proporção de vezes que |diffs| >= |observed_diff|
    p_value = np.mean(np.abs(diffs) >= np.abs(observed_diff))

    return observed_diff, lower_bound, upper_bound, p_value

def validate_logistic_model_compare_auc_bootstrap(df, dependent_var, independent_var, test_size=0.3, random_state=42, n_boot=1000):
    """
    Ajusta um modelo de regressão logística, calcula AUC no treino e teste, IC 95%,
    e compara a diferença entre AUC_treino e AUC_teste usando um teste de bootstrap.
    """

    if dependent_var not in df.columns:
        raise ValueError(f"A variável dependente '{dependent_var}' não existe no DataFrame.")
    if independent_var not in df.columns:
        raise ValueError(f"A variável independente '{independent_var}' não existe no DataFrame.")

    df = df.copy()
    np.random.seed(random_state)
    df['random'] = np.random.rand(len(df))

    train = df.loc[df['random'] > test_size].copy()
    test = df.loc[df['random'] <= test_size].copy()

    X_train = train[[independent_var]]
    y_train = train[dependent_var].values  # vetor numpy
    X_train = sm.add_constant(X_train)

    X_test = test[[independent_var]]
    y_test = test[dependent_var].values  # vetor numpy
    X_test = sm.add_constant(X_test)

    model = sm.Logit(y_train, X_train)
    result = model.fit(disp=False)

    train['Predicted_Prob'] = result.predict(X_train)
    test['Predicted_Prob'] = result.predict(X_test)

    pred_train = train['Predicted_Prob'].values
    pred_test = test['Predicted_Prob'].values

    auc_train = roc_auc_score(y_train, pred_train)
    auc_test = roc_auc_score(y_test, pred_test)

    # Teste de bootstrap para diferença entre AUCs
    observed_diff, diff_lower, diff_upper, p_diff = bootstrap_auc_difference(y_train, pred_train, y_test, pred_test, n_boot=n_boot, random_state=random_state)

    # Calcular IC individuais das AUCs usando método Hanley & McNeil
    def auc_confidence_interval(y_true, y_pred):
        auc_value = roc_auc_score(y_true, y_pred)
        n1 = np.sum(y_true == 1)
        n2 = np.sum(y_true == 0)
        Q1 = auc_value / (2 - auc_value)
        Q2 = (2 * auc_value**2) / (1 + auc_value)
        auc_se = np.sqrt((auc_value * (1 - auc_value) + (n1 - 1)*(Q1 - auc_value**2) + (n2 - 1)*(Q2 - auc_value**2)) / (n1*n2))
        z = norm.ppf(0.975)
        lower_bound = auc_value - z * auc_se
        upper_bound = auc_value + z * auc_se
        lower_bound = max(0, lower_bound)
        upper_bound = min(1, upper_bound)
        # Teste de hipótese (AUC != 0.5)
        z_score = (auc_value - 0.5) / auc_se
        p_value = 2 * (1 - norm.cdf(abs(z_score)))
        return auc_value, auc_se, p_value, lower_bound, upper_bound

    train_auc, train_auc_se, train_p_value, train_lower, train_upper = auc_confidence_interval(y_train, pred_train)
    test_auc, test_auc_se, test_p_value, test_lower, test_upper = auc_confidence_interval(y_test, pred_test)

    validation_table = [
        ["Treino", f"{train_auc:.3f}", f"{train_auc_se:.3f}", f"{train_p_value:.3f}", f"{train_lower:.3f}", f"{train_upper:.3f}"],
        ["Teste", f"{test_auc:.3f}", f"{test_auc_se:.3f}", f"{test_p_value:.3f}", f"{test_lower:.3f}", f"{test_upper:.3f}"],
        ["Diferença (Treino - Teste)", f"{observed_diff:.3f}", "-", f"{p_diff:.3f}", f"{diff_lower:.3f}", f"{diff_upper:.3f}"]
    ]

    print(tabulate(
        validation_table,
        headers=["Amostra", "Área", "Std. Error", "Sig.", "Lower Bound (95%)", "Upper Bound (95%)"],
        tablefmt="grid",
        numalign="center"
    ))
    print("\na. Under the nonparametric assumption")
    print("b. Null hypothesis: true area = 0.5 (para AUC individuais)")
    print("c. Null hypothesis: AUC_train = AUC_test (para diferença)")
    print("d. Diferença: IC 95% bootstrap")
    

    
def compute_auc_ci_multiclass_bootstrap_OLD(
    y_true, 
    pred_probs, 
    n_bootstraps=1000, 
    random_seed=42, 
    multi_class="ovr", 
    average="macro"
):
    """
    Calcula AUC multiclasse (One-vs-Rest ou One-vs-One), média (macro/micro/weighted),
    e seu IC 95% via bootstrap.

    Retorna:
        auc_mean: média da AUC
        se_auc: erro padrão aproximado
        ci_lower: limite inferior (IC95%)
        ci_upper: limite superior (IC95%)
    """
    # Verifica se todos os y_true são inteiros (categorias)
    y_true = np.array(y_true)
    # Precisamos garantir que pred_probs seja um array [n amostras, n_classes]
    # e que y_true tenha mesmo n_classes contidas.
    classes_ = np.unique(y_true)
    rng = np.random.RandomState(random_seed)

    # AUC base
    try:
        auc_base = roc_auc_score(
            y_true, 
            pred_probs, 
            multi_class=multi_class, 
            average=average
        )
    except ValueError:
        # Se for impossível calcular (ex.: uma só classe)
        return np.nan, np.nan, np.nan, np.nan

    # Bootstrap
    bootstrapped_scores = []
    n = len(y_true)
    for _ in range(n_bootstraps):
        # amostragem com reposição
        indices = rng.randint(0, n, n)
        y_boot = y_true[indices]
        p_boot = pred_probs[indices, :]
        try:
            score = roc_auc_score(
                y_boot, 
                p_boot, 
                multi_class=multi_class, 
                average=average
            )
            bootstrapped_scores.append(score)
        except ValueError:
            # ocasionalmente pode dar erro se alguma classe sumir no bootstrap
            # => ignora essa amostra
            continue

    if len(bootstrapped_scores) < 2:
        return auc_base, np.nan, np.nan, np.nan

    auc_array = np.array(bootstrapped_scores)
    auc_mean = auc_array.mean()
    se_auc = auc_array.std(ddof=1)  # desvio padrão amostral
    
    # IC 95%
    z975 = norm.ppf(0.975)
    ci_lower = auc_mean - z975 * se_auc
    ci_upper = auc_mean + z975 * se_auc

    return auc_mean, se_auc, ci_lower, ci_upper


def compute_auc_ci_multiclass_bootstrap(
    y_true, 
    pred_probs, 
    n_bootstraps=1000, 
    random_seed=42, 
    multi_class="ovr", 
    average="macro"
):
    """
    Calcula AUC multiclasse (One-vs-Rest ou One-vs-One), média (macro/micro/weighted),
    e seu IC 95% via bootstrap.

    Retorna:
        auc_mean: média da AUC
        se_auc: erro padrão aproximado
        ci_lower: limite inferior (IC95%)
        ci_upper: limite superior (IC95%)
    """
    # Verifica se todos os y_true são inteiros (categorias)
    y_true = np.array(y_true)
    # Precisamos garantir que pred_probs seja um array [n amostras, n_classes]
    # e que y_true tenha mesmo n_classes contidas.
    classes_ = np.unique(y_true)
    rng = np.random.RandomState(random_seed)

    # AUC base
    try:
        auc_base = roc_auc_score(
            y_true, 
            pred_probs, 
            multi_class=multi_class, 
            average=average
        )
    except ValueError:
        # Se for impossível calcular (ex.: uma só classe)
        return np.nan, np.nan, np.nan, np.nan

    # Bootstrap
    bootstrapped_scores = []
    n = len(y_true)
    for _ in range(n_bootstraps):
        # amostragem com reposição
        indices = rng.randint(0, n, n)
        y_boot = y_true[indices]
        p_boot = pred_probs[indices, :]
        try:
            score = roc_auc_score(
                y_boot, 
                p_boot, 
                multi_class=multi_class, 
                average=average
            )
            bootstrapped_scores.append(score)
        except ValueError:
            # ocasionalmente pode dar erro se alguma classe sumir no bootstrap
            # => ignora essa amostra
            continue

    if len(bootstrapped_scores) < 2:
        return auc_base, np.nan, np.nan, np.nan

    auc_array = np.array(bootstrapped_scores)
    auc_mean = auc_array.mean()
    se_auc = auc_array.std(ddof=1)  # desvio padrão amostral
    
    # IC 95%
    z975 = norm.ppf(0.975)
    ci_lower = auc_mean - z975 * se_auc
    ci_upper = auc_mean + z975 * se_auc

    return auc_mean, se_auc, ci_lower, ci_upper

   
def plot_logits_with_baseline_OLD(
    df, 
    modelo_final, 
    y_col="Chá",         # coluna que contém as categorias (ex.: 1, 2, 3)
    col_expl="Disposição",
    baseline_cat=None
):
    """
    Plota subplots de log(p_A / p_B) em função de col_expl.
    Se baseline_cat for None, gera todos os pares de categorias (combinations).
    Se baseline_cat for definido, gera apenas log(p_cat / p_baseline_cat) para cada cat != baseline_cat.
    
    Parâmetros
    ----------
    df : pd.DataFrame
        DataFrame que contém as colunas necessárias (incluindo y_col e col_expl).
    modelo_final : objeto statsmodels MNLogit (ou similar)
        Modelo multinomial já ajustado, com método .predict().
    y_col : str
        Nome da coluna com as categorias dependentes (ex.: "Chá").
    col_expl : str
        Nome da coluna usada como eixo X (ex.: "Disposição").
    baseline_cat : int ou None
        Se for None, faz gráficos para todos os pares (combinations).
        Se for, por ex., 3, fará log(p_1/p_3), log(p_2/p_3), etc.
        
    Retorna
    -------
    fig : plotly.graph_objs._figure.Figure
        Objeto Plotly com subplots para cada par de categorias (ou baseline).
    """

    # 1) Ordena o DataFrame pela variável explicativa (para plot suave)
    df_sorted = df.sort_values(by=col_expl).copy()

    # 2) Identifica as categorias únicas na coluna y_col
    unique_cats = np.sort(df_sorted[y_col].unique().astype(int))
    # Ex.: [1, 2, 3], ou [0,1,2], etc.

    # 3) Define quais pares iremos comparar
    if baseline_cat is None:
        # Gera todas as combinações 2 a 2
        pairs = list(combinations(unique_cats, 2))
    else:
        # Gera os pares (cat, baseline_cat) para cada cat != baseline_cat
        # Atenção: se você preferir a ordem contrária, troque a tupla
        # (ex. baseline_cat por último ou primeiro).
        pairs = [(cat, baseline_cat) for cat in unique_cats if cat != baseline_cat]
        # Se quiser a baseline sempre no denominador: log(p_cat / p_baseline_cat)

    # 4) Obtém as probabilidades previstas
    predicted_probs = modelo_final.predict(df_sorted)

    # 4a) Verifica quais colunas foram criadas pelo predict
    model_cols = np.sort(predicted_probs.columns)

    # 4b) Se o número de colunas de predicted_probs bate com o número de categorias únicas,
    #     cria um mapeamento para renomear as colunas, igualando-as às categorias do DF.
    if len(model_cols) == len(unique_cats):
        map_dict = {mc: uc for mc, uc in zip(model_cols, unique_cats)}
        predicted_probs = predicted_probs.rename(columns=map_dict)
    else:
        # Caso não bata, avisamos. Ainda tentaremos plotar do jeito que estiver.
        print("[AVISO] Nº de colunas em predicted_probs difere do nº de categorias em y_col.")
        print("        Pode ser que exista baseline interna ou outra codificação no modelo.")
        print(f"        Colunas do modelo: {model_cols}")
        print(f"        Categorias em {y_col}: {unique_cats}")

    # 5) Prepara a figura com subplots
    n_plots = len(pairs)
    subplot_titles = [f"log(p_{a}/p_{b})" for (a,b) in pairs]
    fig = make_subplots(rows=1, cols=n_plots, subplot_titles=subplot_titles)

    # 6) Loop para cada par de categorias
    for i, (catA, catB) in enumerate(pairs, start=1):
        x_vals = df_sorted[col_expl]

        # Extrai pA e pB do DataFrame de probabilidades
        pA = predicted_probs[catA]
        pB = predicted_probs[catB]

        # Calcula log(pA / pB), evitando log(0)
        logit = np.log(pA.replace(0, np.nan) / pB.replace(0, np.nan))

        # a) Plot dos pontos
        fig.add_trace(
            go.Scatter(
                x=x_vals,
                y=logit,
                mode='markers',
                name=f"Logit({catA}/{catB})"
            ),
            row=1, col=i
        )

        # b) Ajuste de regressão linear (exemplo)
        coefs = np.polyfit(x_vals, logit, 1)  # grau 1 => reta
        poly = np.poly1d(coefs)
        y_fit = poly(x_vals)

        # R² simples
        ss_res = np.sum((logit - y_fit)**2)
        ss_tot = np.sum((logit - np.mean(logit))**2)
        r2 = 1 - ss_res / ss_tot if ss_tot != 0 else 0

        # Plota a reta
        fig.add_trace(
            go.Scatter(
                x=x_vals,
                y=y_fit,
                mode='lines',
                name=f"Reg lin ({catA}/{catB})"
            ),
            row=1, col=i
        )

        # c) Anotação da equação + R²
        slope = coefs[0]
        intercept = coefs[1]
        eq_text = (
            f"y = {intercept:.2f} + {slope:.2f}*x<br>"
            f"R² = {r2:.2f}"
        )

        # Posição central (arbitrária)
        x_median = x_vals.median()
        y_median = np.median(logit.dropna())

        fig.add_annotation(
            x=x_median,
            y=y_median,
            text=eq_text,
            showarrow=True,
            arrowhead=2,
            row=1, col=i
        )

        # Ajusta eixos
        fig.update_xaxes(title_text=col_expl, row=1, col=i)
        fig.update_yaxes(title_text=f"log(p_{catA}/p_{catB})", row=1, col=i)

    # 7) Layout final
    if baseline_cat is None:
        big_title = f"Logits (todos os pares) de {y_col} vs {col_expl}"
    else:
        big_title = f"Logits (cat vs. baseline={baseline_cat}) de {y_col} vs {col_expl}"

    fig.update_layout(
        width=1200,
        height=450,
        title=big_title
    )

    return fig.show()

def plot_logits_with_baseline(
    df, 
    modelo_final, 
    y_col="Chá",                # coluna que contém as categorias (ex.: 1, 2, 3)
    col_expl="Disposição",      # pode ser string (única) ou lista de strings
    baseline_cat=None
):
    """
    Plota subplots de log(p_A / p_B) em função de uma ou mais variáveis explicativas.
    Se baseline_cat for None, gera todos os pares de categorias (combinations).
    Se baseline_cat for definido, gera apenas log(p_cat / p_baseline_cat) para cada cat != baseline_cat.
    
    Parâmetros
    ----------
    df : pd.DataFrame
        DataFrame que contém as colunas necessárias (incluindo y_col e col_expl).
    modelo_final : objeto statsmodels MNLogit (ou similar)
        Modelo multinomial já ajustado, com método .predict().
    y_col : str
        Nome da coluna com as categorias dependentes (ex.: "Chá").
    col_expl : str ou list de str
        Nome(s) da(s) coluna(s) usada(s) como eixo X (ex.: "Disposição" ou ["Disposição","OutraVar"]).
    baseline_cat : int ou None
        Se for None, faz gráficos para todos os pares (combinations).
        Se for, por ex., 3, fará log(p_1/p_3), log(p_2/p_3), etc.
        
    Retorna
    -------
    Mostra o gráfico interativo (Plotly) contendo subplots.
    """

    # 1) Se col_expl for string, converte para lista
    if isinstance(col_expl, str):
        col_expl_list = [col_expl]
    else:
        col_expl_list = col_expl

    # 2) Identifica as categorias únicas na coluna y_col
    df_temp = df.copy()
    unique_cats = np.sort(df_temp[y_col].unique().astype(int))
    # Ex.: [1, 2, 3], ou [0,1,2], etc.

    # 3) Define quais pares iremos comparar
    if baseline_cat is None:
        # Gera todas as combinações 2 a 2
        pairs = list(combinations(unique_cats, 2))
    else:
        # Gera os pares (cat, baseline_cat) para cada cat != baseline_cat
        pairs = [(cat, baseline_cat) for cat in unique_cats if cat != baseline_cat]

    n_rows = len(col_expl_list)
    n_cols = len(pairs)

    # 4) Cria títulos para cada subplot
    #    Vamos concatenar a variável explicativa e o par de categorias no título.
    subplot_titles = []
    for ce in col_expl_list:
        for (a, b) in pairs:
            subplot_titles.append(f"{ce}: log(p_{a}/p_{b})")

    # 5) Prepara a figura com subplots (grade: rows x cols)
    fig = make_subplots(rows=n_rows, cols=n_cols, subplot_titles=subplot_titles)

    # 6) Loop principal: para cada variável explicativa (linha) e para cada par (coluna)
    subplot_idx = 0  # indexador para buscar o título correto
    for i, ce in enumerate(col_expl_list, start=1):

        # Ordena o DataFrame pela variável explicativa
        df_sorted = df_temp.sort_values(by=ce).copy()

        # Obtém as probabilidades previstas
        predicted_probs = modelo_final.predict(df_sorted)
        model_cols = np.sort(predicted_probs.columns)

        # Se o número de colunas em predicted_probs bater com o número de categorias únicas,
        # cria um mapeamento para renomear as colunas, igualando-as às categorias do DF.
        if len(model_cols) == len(unique_cats):
            map_dict = {mc: uc for mc, uc in zip(model_cols, unique_cats)}
            predicted_probs = predicted_probs.rename(columns=map_dict)
        else:
            print("[AVISO] Nº de colunas em predicted_probs difere do nº de categorias em y_col.")
            print("        Pode ser que exista baseline interna ou outra codificação no modelo.")
            print(f"        Colunas do modelo: {model_cols}")
            print(f"        Categorias em {y_col}: {unique_cats}")

        for j, (catA, catB) in enumerate(pairs, start=1):
            subplot_idx += 1  # Para pegar o título correto

            x_vals = df_sorted[ce]
            pA = predicted_probs[catA]
            pB = predicted_probs[catB]

            # Calcula log(pA / pB), evitando log(0)
            logit = np.log(pA.replace(0, np.nan) / pB.replace(0, np.nan))

            # a) Plot dos pontos
            fig.add_trace(
                go.Scatter(
                    x=x_vals,
                    y=logit,
                    mode='markers',
                    name=f"Logit({catA}/{catB}) - {ce}",
                    showlegend=False  # Para não repetir a legenda em cada subplot
                ),
                row=i, col=j
            )

            # b) Ajuste de regressão linear (exemplo)
            #    (Cuidado com casos sem pontos ou NaN)
            valid_mask = ~logit.isna()
            if valid_mask.sum() > 1:
                coefs = np.polyfit(x_vals[valid_mask], logit[valid_mask], 1)  # grau 1 => reta
                poly = np.poly1d(coefs)
                y_fit = poly(x_vals)

                # R² simples
                ss_res = np.sum((logit[valid_mask] - y_fit[valid_mask])**2)
                ss_tot = np.sum((logit[valid_mask] - np.mean(logit[valid_mask]))**2)
                r2 = 1 - ss_res / ss_tot if ss_tot != 0 else 0

                # Plota a reta
                fig.add_trace(
                    go.Scatter(
                        x=x_vals,
                        y=y_fit,
                        mode='lines',
                        name=f"Reg lin ({catA}/{catB}) - {ce}",
                        showlegend=False
                    ),
                    row=i, col=j
                )

                # c) Anotação da equação + R²
                slope = coefs[0]
                intercept = coefs[1]
                eq_text = (
                    f"y = {intercept:.2f} + {slope:.2f}*x<br>"
                    f"R² = {r2:.2f}"
                )

                x_median = x_vals.median()
                y_median = np.median(logit.dropna())
                fig.add_annotation(
                    x=x_median,
                    y=y_median,
                    text=eq_text,
                    showarrow=True,
                    arrowhead=2,
                    row=i, col=j
                )
            else:
                # Se houver poucos ou nenhum ponto válido para regressão
                fig.add_annotation(
                    x=0.5,
                    y=0.5,
                    text="Poucos dados ou NaNs para regressão",
                    showarrow=False,
                    xref=f"x domain",
                    yref=f"y domain",
                    row=i, col=j
                )

            # Ajusta eixos
            fig.update_xaxes(title_text=ce, row=i, col=j)
            fig.update_yaxes(title_text=f"log(p_{catA}/p_{catB})", row=i, col=j)

    # 7) Layout final
    if baseline_cat is None:
        big_title = f"Logits (todos os pares) de {y_col} vs múltiplas variáveis"
    else:
        big_title = f"Logits (cat vs. baseline={baseline_cat}) de {y_col} vs múltiplas variáveis"

    # Ajustando tamanho de acordo com nº de subplots
    fig_width = 300 * n_cols
    fig_height = 400 * n_rows

    fig.update_layout(
        width=fig_width,
        height=fig_height,
        title=big_title
    )

    return fig.show()


def plot_predicted_probabilities_OLD(
    df,
    modelo_final,
    col_expl="Disposição",
    palette=None,
    fig_width=900,
    fig_height=500
):
    """
    Plota as Probabilidades Previstas de cada categoria de um modelo
    de Regressão Logística Multinomial (statsmodels MNLogit) em função
    de uma variável explicativa (col_expl).

    Parâmetros
    ----------
    df : pd.DataFrame
        DataFrame com as colunas necessárias para o modelo. Deve conter col_expl.
    modelo_final : statsmodels MNLogit
        Modelo multinomial já ajustado, com método .predict().
    col_expl : str, padrão="Disposição"
        Nome da variável independente que será o eixo X.
    palette : list ou None
        Lista de cores a ser utilizada (uma para cada categoria). Se None,
        usa `plotly.colors.qualitative.Plotly`.
    fig_width : int, padrão=900
        Largura (em pixels) do gráfico final.
    fig_height : int, padrão=500
        Altura (em pixels) do gráfico final.

    Retorno
    -------
    fig : plotly.graph_objs._figure.Figure
        Objeto Plotly com o subplot das probabilidades.
    """

    # 1) Verifica se col_expl existe
    if col_expl not in df.columns:
        raise ValueError(f"A coluna '{col_expl}' não existe no DataFrame.")

    # 2) Ordena o DataFrame pela variável explicativa (para plotar curvas "suaves")
    df_sorted = df.sort_values(by=col_expl).copy()

    # 3) Obtém as probabilidades previstas para cada categoria
    predicted_probs = modelo_final.predict(df_sorted)
    categorias = predicted_probs.columns  # podem ser [0,1,2], ou [1,2,3], etc.

    # 4) Define a paleta de cores
    if palette is None:
        palette = qualitative.Plotly  # Ex.: ['#636EFA', '#EF553B', ...]
    
    # Mapeamento categoria -> cor
    cat_color_map = {}
    for i, cat in enumerate(categorias):
        cat_color_map[cat] = palette[i % len(palette)]

    # 5) Cria uma única subplot
    fig = make_subplots(rows=1, cols=1, subplot_titles=[f"Probabilidades Previstas vs {col_expl}"])
    
    # 6) Adiciona um Scatter para cada categoria
    for cat in categorias:
        fig.add_trace(
            go.Scatter(
                x=df_sorted[col_expl],
                y=predicted_probs[cat],
                mode='lines',
                name=f"Prob Cat {cat}",
                line=dict(color=cat_color_map[cat])
            ),
            row=1, col=1
        )

    # 7) Ajusta eixos
    fig.update_xaxes(title_text=col_expl, row=1, col=1)
    fig.update_yaxes(title_text="Predicted Probability", row=1, col=1)

    # 8) Layout final
    fig.update_layout(
        width=fig_width,
        height=fig_height,
        title=f"Multinomial Logistic - Probabilidades Previstas ({col_expl})",
        legend=dict(x=1.02, y=1, xanchor='left', yanchor='top')
    )

    return fig.show()

def plot_predicted_probabilities_OLD2(
    df,
    modelo_final,
    col_expl,   # Agora pode ser uma lista de variáveis explicativas
    palette=None,
    fig_width=900,
    fig_height=500
):
    """
    Plota as Probabilidades Previstas de cada categoria de um modelo
    de Regressão Logística Multinomial (statsmodels MNLogit) em função
    de uma ou mais variáveis explicativas.

    Se `col_expl` for uma lista, gera um gráfico separado para cada variável.

    Parâmetros
    ----------
    df : pd.DataFrame
        DataFrame com as colunas necessárias para o modelo.
    modelo_final : statsmodels MNLogit
        Modelo multinomial já ajustado, com método .predict().
    col_expl : str ou list de str
        Nome(s) da(s) variável(is) independente(s) que será(ão) o eixo X.
    palette : list ou None
        Lista de cores a ser utilizada (uma para cada categoria). Se None,
        usa `plotly.colors.qualitative.Plotly`.
    fig_width : int, padrão=900
        Largura (em pixels) do gráfico final.
    fig_height : int, padrão=500
        Altura (em pixels) do gráfico final.

    Retorno
    -------
    Mostra um gráfico separado para cada variável explicativa.
    """

    # 1) Se col_expl for string, converte para lista
    if isinstance(col_expl, str):
        col_expl = [col_expl]

    # 2) Define paleta de cores
    if palette is None:
        palette = qualitative.Plotly  # Ex.: ['#636EFA', '#EF553B', ...]

    # 3) Descobre as categorias a partir de uma chamada ao modelo
    df_temp = df.copy()
    predicted_probs_temp = modelo_final.predict(df_temp)
    categorias = predicted_probs_temp.columns  # podem ser [0,1,2], ou [1,2,3], etc.

    # 4) Mapeamento categoria -> cor
    cat_color_map = {cat: palette[i % len(palette)] for i, cat in enumerate(categorias)}

    # 5) Loop sobre cada variável explicativa
    for ce in col_expl:
        # Ordena o DF pela variável atual
        df_sorted_ce = df_temp.sort_values(by=ce).copy()
        predicted_probs = modelo_final.predict(df_sorted_ce)

        # Cria nova figura
        fig = go.Figure()

        # Adiciona um Scatter para cada categoria
        for cat in categorias:
            fig.add_trace(
                go.Scatter(
                    x=df_sorted_ce[ce],
                    y=predicted_probs[cat],
                    mode='lines',
                    name=f"Prob Cat {cat}",
                    line=dict(color=cat_color_map[cat])
                )
            )

        # Ajusta layout da figura
        fig.update_layout(
            width=fig_width,
            height=fig_height,
            title=f"Probabilidades Previstas vs {ce}",
            xaxis_title=ce,
            yaxis_title="Predicted Probability"
        )

        # Exibe o gráfico para esta variável
        fig.show()
        
        
def generate_terms_OLD(base_predictors):
    """
    Gera a lista de termos (variáveis principais + interações de todas as ordens)
    a partir de uma lista de preditores base.
    
    Exemplo:
      base_predictors = ["Residência", "Cidadãos", "Viagens"]
      Retorna [
        "Residência", "Cidadãos", "Viagens",
        "Residência:Cidadãos", "Residência:Viagens", "Cidadãos:Viagens",
        "Residência:Cidadãos:Viagens"
      ]
    """
    terms = []
    n = len(base_predictors)
    # Efeitos principais
    for bp in base_predictors:
        terms.append(bp)
    # Interações (até a ordem máxima = n)
    for r in range(2, n+1):
        for combo in combinations(base_predictors, r):
            terms.append(":".join(combo))
    return terms

from itertools import combinations

def generate_terms(independent_numerical_vars, independent_categorical_vars):
    """
    Gera a lista de termos (variáveis principais + interações de todas as ordens)
    a partir de listas separadas de preditores numéricos e categóricos.
    
    Exemplo:
      independent_numerical_vars = ["Viagens"]
      independent_categorical_vars = ["Residência", "Cidadãos"]
      Retorna [
        "Residência", "Cidadãos", "Viagens",
        "Residência:Cidadãos", "Residência:Viagens", "Cidadãos:Viagens",
        "Residência:Cidadãos:Viagens"
      ]
    """
    # Combina as variáveis categóricas e numéricas
    base_predictors = independent_numerical_vars + independent_categorical_vars
    
    # Se não houver preditores, retorna lista vazia
    if not base_predictors:
        return []
    
    terms = []
    n = len(base_predictors)
    
    # Efeitos principais
    terms.extend(base_predictors)
    
    # Interações (até a ordem máxima = n)
    for r in range(2, n + 1):
        for combo in combinations(base_predictors, r):
            terms.append(":".join(combo))
    
    return terms

def build_formula_V12022025(dependent_var, predictors, include_intercept=True, output_format='patsy'):
    """
    Constrói fórmula adicionando C(...) às variáveis categóricas no estilo Patsy,
    inclusive em interações, ou retorna no formato não-Patsy.
    
    Parâmetros:
    - dependent_var: variável dependente.
    - predictors: lista de variáveis preditoras.
    - include_intercept: inclui ou não o intercepto na fórmula.
    - output_format: 'patsy' para formato Patsy, 'plain' para formato não-Patsy.
      O padrão é 'patsy'.
    
    Retorna:
    - String da fórmula no formato especificado.
    """
    if output_format not in {'patsy', 'plain'}:
        raise ValueError("output_format deve ser 'patsy' ou 'plain'")
    
    if not predictors:
        # Modelo sem preditores SEMPRE precisa de ~1 (intercepto)
        formula = f"{dependent_var} ~ 1"
        return formula
    
    if output_format == 'patsy':
        formatted = [":".join(f"C({x})" for x in p.split(":")) for p in predictors]
    else:
        formatted = predictors  # No formato 'plain', mantém a sintaxe original
    
    formula = f"{dependent_var} ~ 1 + {' + '.join(formatted)}"
    
    if not include_intercept:
        formula = formula.replace(" ~ 1 + ", " ~ 0 + ")
    
    return formula

def build_formula(dependent_var, independent_numerical_vars, independent_categorical_vars, selected_predictors, include_intercept=True, output_format='patsy'):
    """
    Constrói fórmula adicionando C(...) às variáveis categóricas no estilo Patsy,
    inclusive em interações, ou retorna no formato não-Patsy, considerando apenas os preditores selecionados.

    Parâmetros:
    - dependent_var: variável dependente.
    - independent_numerical_vars: lista de variáveis numéricas.
    - independent_categorical_vars: lista de variáveis categóricas.
    - selected_predictors: lista de preditores de interesse, incluindo interações.
    - include_intercept: inclui ou não o intercepto na fórmula.
    - output_format: 'patsy' para formato Patsy, 'plain' para formato não-Patsy.
      O padrão é 'patsy'.

    Retorna:
    - String da fórmula no formato especificado.
    """
    if output_format not in {'patsy', 'plain'}:
        raise ValueError("output_format deve ser 'patsy' ou 'plain'")

    if not selected_predictors:
        return f"{dependent_var} ~ 1"  # Modelo sem preditores sempre precisa de ~1 (intercepto)

    if output_format == 'patsy':
        formatted = [
            ":".join(f"C({var})" if var in independent_categorical_vars else var for var in term.split(":"))
            for term in selected_predictors
        ]
    else:
        formatted = selected_predictors  # No formato 'plain', mantém a sintaxe original

    formula = f"{dependent_var} ~ 1 + {' + '.join(formatted)}"

    if not include_intercept:
        formula = formula.replace(" ~ 1 + ", " ~ 0 + ")

    return formula



def build_formula_NEW(dependent_var, predictors, include_intercept=True, output_format='patsy', data=None):
    """
    Constrói uma fórmula para modelos estatísticos. Quando output_format for 'patsy',
    adiciona C(...) automaticamente às variáveis categóricas (baseado nos dtypes do DataFrame 'data')
    e mantém preditores contínuos sem transformação, inclusive em interações.
    
    Parâmetros:
    - dependent_var: string com o nome da variável dependente.
    - predictors: lista de strings com os nomes dos preditores; pode conter interações separadas por ':'.
    - include_intercept: se True, inclui intercepto; se False, remove-o (usando 0 + ...).
    - output_format: 'patsy' (formata as variáveis com C(...)) ou 'plain' (mantém os nomes originais).
    - data: DataFrame opcional contendo as variáveis. Se fornecido, os dtypes serão inspecionados
      para determinar se cada variável é categórica (não numérica) ou contínua.
    
    Retorna:
    - String da fórmula no formato especificado.
    """
    if output_format not in {'patsy', 'plain'}:
        raise ValueError("output_format deve ser 'patsy' ou 'plain'")
    
    if not predictors:
        # Mesmo sem preditores, precisamos de um termo (intercepto) no modelo
        return f"{dependent_var} ~ 1"
    
    if output_format == 'patsy':
        formatted = []
        # Se um DataFrame for fornecido, importamos a função para testar tipos
        if data is not None:
            import pandas.api.types as ptypes
        for p in predictors:
            # Trata possíveis interações (ex: "idade:sexo")
            partes = p.split(":")
            partes_formatadas = []
            for var in partes:
                var = var.strip()
                if data is not None and var in data.columns:
                    # Se a variável não é numérica, consideramos categórica
                    if not ptypes.is_numeric_dtype(data[var]):
                        partes_formatadas.append(f"C({var})")
                    else:
                        partes_formatadas.append(var)
                else:
                    # Sem informação (ou data não foi fornecido), assume-se que é contínua
                    partes_formatadas.append(var)
            formatted.append(":".join(partes_formatadas))
    else:
        # No formato 'plain' retorna os nomes como estão
        formatted = predictors

    formula = f"{dependent_var} ~ 1 + {' + '.join(formatted)}"
    if not include_intercept:
        # Remove o intercepto substituindo "1 +" por "0 +"
        formula = formula.replace(" ~ 1 + ", " ~ 0 + ")
    
    return formula

def logistic_regression_odds_summary_OLD(modelo_final):
    coefs = modelo_final.params
    ses = modelo_final.bse
    tvals = modelo_final.tvalues
    pvals = modelo_final.pvalues
    wald_stats = tvals ** 2

    conf_int = modelo_final.conf_int().reset_index()
    conf_int.columns = ["variable", "lower", "upper"]
    conf_int["variable"] = conf_int["variable"].astype(str).str.strip()
    
    table_list = []
    for param in coefs.index:
        param_str = str(param).strip()

        b = coefs.loc[param]
        se = ses.loc[param]
        wald = wald_stats.loc[param]
        pval = pvals.loc[param]
        
        ci_row = conf_int[conf_int["variable"] == param_str]
        if not ci_row.empty:
            ci_lower = ci_row.iloc[0]["lower"]
            ci_upper = ci_row.iloc[0]["upper"]
        else:
            ci_lower, ci_upper = np.nan, np.nan
        
        if "Intercept" in param_str:
            expb = expb_lower = expb_upper = np.nan
        else:
            expb = np.exp(b)
            expb_lower = np.exp(ci_lower) if not np.isnan(ci_lower) else np.nan
            expb_upper = np.exp(ci_upper) if not np.isnan(ci_upper) else np.nan

        table_list.append([
            param_str, b, se, wald, 1, "<0.001" if pval < 0.001 else f"{pval:.4g}",
            expb, expb_lower, expb_upper
        ])
    
    df_table = pd.DataFrame(table_list, columns=[
        "Variable", "B", "Std. Error", "Wald", "df", "Sig.",
        "Exp(B)", "Lower Bound", "Upper Bound"
    ])
    
    df_table[["B", "Std. Error"]] = df_table[["B", "Std. Error"]].round(5)
    df_table[["Wald", "Exp(B)", "Lower Bound", "Upper Bound"]] = df_table[["Wald", "Exp(B)", "Lower Bound", "Upper Bound"]].round(3)
    
    mask_intercept = df_table["Variable"].str.contains("Intercept", case=False)
    df_table.loc[mask_intercept, ["Exp(B)", "Lower Bound", "Upper Bound"]] = np.nan
    
    print("\n=== ESTIMATED PARAMETERS TABLE ===")
    print(
        tabulate(
            df_table,
            headers="keys",
            tablefmt="grid",
            numalign="center",
            floatfmt=".3f",
            showindex=False
        )
    )
    

def logistic_regression_odds_summary_V12022025(modelo_final, model_type='multinomial'):
    """
    Exibe uma tabela com os parâmetros estimados do modelo (coeficientes, erro padrão, estatística Wald, 
    p-valores e intervalos de confiança transformados em Odds Ratio) de forma geral para modelos 
    binomiais, multinomiais e ordinais.

    Parâmetros
    ----------
    modelo_final : objeto statsmodels ajustado
        Modelo final ajustado.
    model_type : str, opcional
        Tipo do modelo. Valores esperados:
         - "binary" para modelos binomiais,
         - "multinomial" para modelos multinomiais,
         - "ordinal" para modelos ordinais.
         O padrão é "multinomial".

    Para modelos binomiais, gera uma tabela única.
    Para modelos multinomiais/ordinais, gera uma tabela separada para cada outcome.
    """
    
    # Função auxiliar para obter os limites de confiança:
    def get_conf_int(conf_int_df, param_str, b, se):
        """
        Tenta extrair o intervalo de confiança para um parâmetro.
        Se não for possível ou se os limites forem NaN, calcula manualmente como b ± 1.96*se.
        """
        ci_row = conf_int_df[conf_int_df["variable"] == param_str]
        if not ci_row.empty:
            ci_lower = ci_row.iloc[0]["lower"]
            ci_upper = ci_row.iloc[0]["upper"]
        else:
            ci_lower, ci_upper = np.nan, np.nan
        if np.isnan(ci_lower) or np.isnan(ci_upper):
            ci_lower = b - 1.96 * se
            ci_upper = b + 1.96 * se
        return ci_lower, ci_upper

    if model_type == 'binary':
        # Espera que os parâmetros estejam em um objeto Series.
        coefs = modelo_final.params
        ses = modelo_final.bse
        tvals = modelo_final.tvalues
        pvals = modelo_final.pvalues
        wald_stats = tvals ** 2

        # Obtém e formata os intervalos de confiança
        conf_int = modelo_final.conf_int().reset_index()
        if conf_int.shape[1] == 3:
            conf_int.columns = ["variable", "lower", "upper"]
        elif conf_int.shape[1] >= 4:
            # Usa apenas as 3 primeiras colunas: a coluna de variável, lower e upper.
            conf_int = conf_int.iloc[:, :3]
            conf_int.columns = ["variable", "lower", "upper"]
        conf_int["variable"] = conf_int["variable"].astype(str).str.strip()

        table_list = []
        for param in coefs.index:
            param_str = str(param).strip()
            b = coefs.loc[param]
            se = ses.loc[param]
            wald = wald_stats.loc[param]
            pval = pvals.loc[param]
            
            ci_lower, ci_upper = get_conf_int(conf_int, param_str, b, se)
            
            if "Intercept" in param_str:
                expb = expb_lower = expb_upper = np.nan
            else:
                expb = np.exp(b)
                expb_lower = np.exp(ci_lower)
                expb_upper = np.exp(ci_upper)
            
            table_list.append([
                param_str, b, se, wald, 1,
                "<0.001" if pval < 0.001 else f"{pval:.4g}",
                expb, expb_lower, expb_upper
            ])
        
        df_table = pd.DataFrame(table_list, columns=[
            "Variable", "B", "Std. Error", "Wald", "df", "Sig.",
            "Exp(B)", "Lower Bound", "Upper Bound"
        ])
        
        df_table[["B", "Std. Error"]] = df_table[["B", "Std. Error"]].round(5)
        df_table[["Wald", "Exp(B)", "Lower Bound", "Upper Bound"]] = df_table[["Wald", "Exp(B)", "Lower Bound", "Upper Bound"]].round(3)
        mask_intercept = df_table["Variable"].str.contains("Intercept", case=False)
        df_table.loc[mask_intercept, ["Exp(B)", "Lower Bound", "Upper Bound"]] = np.nan
        
        print("\n=== ESTIMATED PARAMETERS TABLE (Binary Model) ===")
        print(tabulate(df_table, headers="keys", tablefmt="grid", numalign="center", floatfmt=".3f", showindex=False))
    
    elif model_type in ['multinomial', 'ordinal']:
        # Espera que os parâmetros estejam em um DataFrame, com cada coluna representando um outcome.
        outcomes = modelo_final.params.columns
        for outcome in outcomes:
            coefs = modelo_final.params[outcome]
            ses = modelo_final.bse[outcome]
            tvals = modelo_final.tvalues[outcome]
            pvals = modelo_final.pvalues[outcome]
            wald_stats = tvals ** 2
            
            # Obtém os intervalos de confiança para o outcome.
            conf_int = modelo_final.conf_int()
            if isinstance(conf_int.columns, pd.MultiIndex):
                # Supõe que o primeiro nível corresponde ao outcome e o segundo a "lower"/"upper"
                conf_int_outcome = conf_int.xs(outcome, axis=1, level=0).reset_index()
                conf_int_outcome.columns = ["variable", "lower", "upper"]
            else:
                temp = conf_int.reset_index()
                if temp.shape[1] == 3:
                    temp.columns = ["variable", "lower", "upper"]
                elif temp.shape[1] >= 4:
                    temp = temp.iloc[:, :3]
                    temp.columns = ["variable", "lower", "upper"]
                conf_int_outcome = temp
            
            conf_int_outcome["variable"] = conf_int_outcome["variable"].astype(str).str.strip()
            
            table_list = []
            for param in coefs.index:
                param_str = str(param).strip()
                b = coefs.loc[param]
                se = ses.loc[param]
                wald = wald_stats.loc[param]
                pval = pvals.loc[param]
                
                ci_lower, ci_upper = get_conf_int(conf_int_outcome, param_str, b, se)
                
                if "Intercept" in param_str:
                    expb = expb_lower = expb_upper = np.nan
                else:
                    expb = np.exp(b)
                    expb_lower = np.exp(ci_lower)
                    expb_upper = np.exp(ci_upper)
                
                table_list.append([
                    param_str, b, se, wald, 1,
                    "<0.001" if pval < 0.001 else f"{pval:.4g}",
                    expb, expb_lower, expb_upper
                ])
            
            df_table = pd.DataFrame(table_list, columns=[
                "Variable", "B", "Std. Error", "Wald", "df", "Sig.",
                "Exp(B)", "Lower Bound", "Upper Bound"
            ])
            
            df_table[["B", "Std. Error"]] = df_table[["B", "Std. Error"]].round(5)
            df_table[["Wald", "Exp(B)", "Lower Bound", "Upper Bound"]] = df_table[["Wald", "Exp(B)", "Lower Bound", "Upper Bound"]].round(3)
            mask_intercept = df_table["Variable"].str.contains("Intercept", case=False)
            df_table.loc[mask_intercept, ["Exp(B)", "Lower Bound", "Upper Bound"]] = np.nan
            
            print(f"\n=== ESTIMATED PARAMETERS TABLE for outcome: {outcome} ({model_type.title()} Model) ===")
            print(tabulate(df_table, headers="keys", tablefmt="grid", numalign="center", floatfmt=".3f", showindex=False))
    else:
        print("Modelo com parâmetro 'model_type' desconhecido. Use 'binary', 'multinomial' ou 'ordinal'.")

def logistic_regression_odds_summary(modelo_final, model_type='multinomial'):
    """
    Exibe uma tabela com os parâmetros estimados do modelo (coeficientes, erro padrão, estatística Wald, 
    p-valores e intervalos de confiança transformados em Odds Ratio) para modelos binomiais, multinomiais e ordinais.
    """
    
    def get_conf_int(conf_int_df, param_str, b, se):
        # Tenta extrair o intervalo de confiança para um parâmetro. Caso contrário, calcula como b ± 1.96*se.
        ci_row = conf_int_df[conf_int_df["variable"] == param_str]
        if not ci_row.empty:
            ci_lower = ci_row.iloc[0]["lower"]
            ci_upper = ci_row.iloc[0]["upper"]
        else:
            ci_lower, ci_upper = np.nan, np.nan
        if np.isnan(ci_lower) or np.isnan(ci_upper):
            ci_lower = b - 1.96 * se
            ci_upper = b + 1.96 * se
        return ci_lower, ci_upper

    if model_type == 'binary':
        # Bloco para modelos binomiais (Series)
        coefs = modelo_final.params
        ses = modelo_final.bse
        tvals = modelo_final.tvalues
        pvals = modelo_final.pvalues
        wald_stats = tvals ** 2

        conf_int = modelo_final.conf_int().reset_index()
        if conf_int.shape[1] == 3:
            conf_int.columns = ["variable", "lower", "upper"]
        elif conf_int.shape[1] >= 4:
            conf_int = conf_int.iloc[:, :3]
            conf_int.columns = ["variable", "lower", "upper"]
        conf_int["variable"] = conf_int["variable"].astype(str).str.strip()

        table_list = []
        for param in coefs.index:
            param_str = str(param).strip()
            b = coefs.loc[param]
            se = ses.loc[param]
            wald = wald_stats.loc[param]
            pval = pvals.loc[param]

            ci_lower, ci_upper = get_conf_int(conf_int, param_str, b, se)

            if "Intercept" in param_str:
                expb = expb_lower = expb_upper = np.nan
            else:
                expb = np.exp(b)
                expb_lower = np.exp(ci_lower)
                expb_upper = np.exp(ci_upper)

            table_list.append([
                param_str, b, se, wald, 1,
                "<0.001" if pval < 0.001 else f"{pval:.4g}",
                expb, expb_lower, expb_upper
            ])

        df_table = pd.DataFrame(table_list, columns=[
            "Variable", "B", "Std. Error", "Wald", "df", "Sig.",
            "Exp(B)", "Lower Bound", "Upper Bound"
        ])

        df_table[["B", "Std. Error"]] = df_table[["B", "Std. Error"]].round(5)
        df_table[["Wald", "Exp(B)", "Lower Bound", "Upper Bound"]] = df_table[["Wald", "Exp(B)", "Lower Bound", "Upper Bound"]].round(3)
        mask_intercept = df_table["Variable"].str.contains("Intercept", case=False)
        df_table.loc[mask_intercept, ["Exp(B)", "Lower Bound", "Upper Bound"]] = np.nan

        print("\n=== ESTIMATED PARAMETERS TABLE (Binary Model) ===")
        print(tabulate(df_table, headers="keys", tablefmt="grid", numalign="center", floatfmt=".3f", showindex=False))

    elif model_type in ['multinomial', 'ordinal']:
        # Verifica se os parâmetros estão em um DataFrame ou em uma Series:
        outcomes = modelo_final.params.columns if hasattr(modelo_final.params, 'columns') else [None]

        for outcome in outcomes:
            if outcome is None:
                # Trata o caso em que os parâmetros estão em uma Series (único outcome)
                coefs = modelo_final.params
                ses = modelo_final.bse
                tvals = modelo_final.tvalues
                pvals = modelo_final.pvalues
                conf_int = modelo_final.conf_int().reset_index()
            else:
                coefs = modelo_final.params[outcome]
                ses = modelo_final.bse[outcome]
                tvals = modelo_final.tvalues[outcome]
                pvals = modelo_final.pvalues[outcome]
                conf_int = modelo_final.conf_int()
                if isinstance(conf_int.columns, pd.MultiIndex):
                    conf_int = conf_int.xs(outcome, axis=1, level=0).reset_index()
                else:
                    conf_int = conf_int.reset_index()

            # Ajusta os nomes das colunas do intervalo de confiança
            if conf_int.shape[1] >= 3:
                conf_int = conf_int.iloc[:, :3]
                conf_int.columns = ["variable", "lower", "upper"]
            conf_int["variable"] = conf_int["variable"].astype(str).str.strip()

            wald_stats = tvals ** 2

            table_list = []
            for param in coefs.index:
                param_str = str(param).strip()
                b = coefs.loc[param]
                se = ses.loc[param]
                wald = wald_stats.loc[param]
                pval = pvals.loc[param]

                ci_lower, ci_upper = get_conf_int(conf_int, param_str, b, se)

                if "Intercept" in param_str:
                    expb = expb_lower = expb_upper = np.nan
                else:
                    expb = np.exp(b)
                    expb_lower = np.exp(ci_lower)
                    expb_upper = np.exp(ci_upper)

                table_list.append([
                    param_str, b, se, wald, 1,
                    "<0.001" if pval < 0.001 else f"{pval:.4g}",
                    expb, expb_lower, expb_upper
                ])

            df_table = pd.DataFrame(table_list, columns=[
                "Variable", "B", "Std. Error", "Wald", "df", "Sig.",
                "Exp(B)", "Lower Bound", "Upper Bound"
            ])

            df_table[["B", "Std. Error"]] = df_table[["B", "Std. Error"]].round(5)
            df_table[["Wald", "Exp(B)", "Lower Bound", "Upper Bound"]] = df_table[["Wald", "Exp(B)", "Lower Bound", "Upper Bound"]].round(3)
            mask_intercept = df_table["Variable"].str.contains("Intercept", case=False)
            df_table.loc[mask_intercept, ["Exp(B)", "Lower Bound", "Upper Bound"]] = np.nan

            if outcome is None:
                print("\n=== ESTIMATED PARAMETERS TABLE (Ordinal Model) ===")
            else:
                print(f"\n=== ESTIMATED PARAMETERS TABLE for outcome: {outcome} ({model_type.title()} Model) ===")
            print(tabulate(df_table, headers="keys", tablefmt="grid", numalign="center", floatfmt=".3f", showindex=False))
    else:
        print("Modelo com parâmetro 'model_type' desconhecido. Use 'binary', 'multinomial' ou 'ordinal'.")


    
def goodness_of_fit(modelo_intercept_only, modelo_saturated, modelo_stepwise):
    """
    Avalia a qualidade do ajuste de três modelos estatísticos usando métricas como AIC, BIC e -2LL,
    além de calcular a razão de verossimilhança entre os modelos.

    Parâmetros:
    modelo_intercept_only : Modelo estatístico contendo apenas o intercepto.
    modelo_saturated : Modelo estatístico saturado, ou seja, com todos os parâmetros possíveis.
    modelo_stepwise : Modelo estatístico final após a seleção de variáveis.

    Retorno:
    Exibe uma tabela formatada com os valores de ajuste e significância estatística.
    """

    def compute_model_metrics(model):
        return {
            'AIC': model.aic,
            'BIC': model.bic,
            '-2LL': -2 * model.llf if hasattr(model, "llf") else np.nan,
            'df_model': model.df_model if hasattr(model, "df_model") else np.nan,
            'llf': model.llf if hasattr(model, "llf") else np.nan
        }
    
    metrics_intercept_only = compute_model_metrics(modelo_intercept_only)
    metrics_saturated = compute_model_metrics(modelo_saturated)
    metrics_stepwise = compute_model_metrics(modelo_stepwise)

    # Cálculo da razão de verossimilhança
    lr_intercept_stepwise = 2 * ((metrics_stepwise['llf'] or 0) - (metrics_intercept_only['llf'] or 0))
    df_intercept_stepwise = (metrics_stepwise['df_model'] or 0) - (metrics_intercept_only['df_model'] or 0)
    p_intercept_stepwise = chi2.sf(lr_intercept_stepwise, df_intercept_stepwise) if df_intercept_stepwise > 0 else np.nan

    lr_stepwise_saturated = 2 * ((metrics_saturated['llf'] or 0) - (metrics_stepwise['llf'] or 0))
    df_stepwise_saturated = (metrics_saturated['df_model'] or 0) - (metrics_stepwise['df_model'] or 0)
    p_stepwise_saturated = chi2.sf(lr_stepwise_saturated, df_stepwise_saturated) if df_stepwise_saturated > 0 else np.nan

    goodness_data = [
        ["Intercept Only",
         metrics_intercept_only['AIC'],
         metrics_intercept_only['BIC'],
         metrics_intercept_only['-2LL'],
         "-", "-", "-"],
        ["Saturated",
         metrics_saturated['AIC'],
         metrics_saturated['BIC'],
         metrics_saturated['-2LL'],
         f"{lr_stepwise_saturated:.3f}",
         df_stepwise_saturated,
         f"{p_stepwise_saturated:.4f}" if p_stepwise_saturated >= 0.001 else "<0.001" if p_stepwise_saturated is not None else "NaN"],
        ["Stepwise",
         metrics_stepwise['AIC'],
         metrics_stepwise['BIC'],
         metrics_stepwise['-2LL'],
         f"{lr_intercept_stepwise:.3f}",
         df_intercept_stepwise,
         f"{p_intercept_stepwise:.4f}" if p_intercept_stepwise >= 0.001 else "<0.001" if p_intercept_stepwise is not None else "NaN"]
    ]

    print("\n=== Goodness of Fit ===")
    print(tabulate(
        goodness_data,
        headers=["Model", "AIC", "BIC", "-2LL", "Chi-Square", "df", "Sig."],
        tablefmt="grid",
        floatfmt=".3f"
    ))

def split_dataset(data, test_size=0.2, random_state=42):
    if not isinstance(data, pd.DataFrame):
        raise ValueError("O parâmetro 'data' deve ser um pandas DataFrame.")
    
    if not (0 < test_size < 1):
        raise ValueError("O parâmetro 'test_size' deve estar entre 0 e 1.")

    np.random.seed(random_state)
    shuffled_indices = np.random.permutation(len(data))
    test_set_size = int(len(data) * test_size)

    test_indices = shuffled_indices[:test_set_size]
    train_indices = shuffled_indices[test_set_size:]

    train = data.iloc[train_indices].copy()
    test = data.iloc[test_indices].copy()
    
    return train, test
    
def auc_roc_table(model, data_train, dependent_var):
    """
    Calcula a AUC-ROC no conjunto de treino com intervalo de confiança de 95% e exibe uma tabela.

    Parâmetros:
    - model: Modelo treinado com método predict_proba() ou predict().
    - data_train: DataFrame contendo os dados de treino, incluindo a variável dependente.
    - dependent_var: Nome da variável dependente (target) no DataFrame.

    Retorno:
    - Exibe a tabela formatada da AUC-ROC com intervalo de confiança de 95%.
    """

    # Separa X_train (features) e y_train (target)
    X_train = data_train.drop(columns=[dependent_var])
    y_train = data_train[dependent_var]

    # Verifica se o modelo tem predict_proba() ou apenas predict()
    if hasattr(model, "predict_proba"):
        y_pred_probs = model.predict_proba(X_train)[:, 1]  # Probabilidade da classe positiva
    else:
        y_pred_probs = model.predict(X_train)  # Usa predição binária diretamente

    # Calcula AUC-ROC
    auc_value = roc_auc_score(y_train, y_pred_probs)

    # Número de instâncias das classes positiva e negativa
    n1, n2 = np.sum(y_train == 1), np.sum(y_train == 0)
    if n1 == 0 or n2 == 0:
        raise ValueError("Classes positivas e negativas não podem estar vazias.")

    # Fórmulas de Hanley & McNeil (1982) para erro padrão da AUC
    Q1 = auc_value / (2 - auc_value)
    Q2 = (2 * auc_value**2) / (1 + auc_value)
    auc_se = np.sqrt((auc_value * (1 - auc_value) + (n1 - 1) * (Q1 - auc_value**2) + (n2 - 1) * (Q2 - auc_value**2)) / (n1*n2))

    # Intervalo de confiança de 95%
    z = 1.96  # Valor crítico para IC 95%
    lower_bound, upper_bound = max(0, auc_value - z * auc_se), min(1, auc_value + z * auc_se)

    # Teste de p-valor para hipótese nula: AUC == 0.5
    z_value = (auc_value - 0.5) / auc_se
    p_value = 2 * (1 - norm.cdf(abs(z_value)))

    # Exibe tabela formatada
    print("\n=== AUC-ROC (TREINO) (com IC 95%) ===")
    auc_table = [
        ["Área (AUC)", "Erro Padrão", "95% IC Inferior", "95% IC Superior", "Significância"],
        [f"{auc_value:.3f}", f"{auc_se:.4f}", f"{lower_bound:.3f}", f"{upper_bound:.3f}", f"{p_value:.3f}"]
    ]
    print(tabulate(auc_table, headers="firstrow", tablefmt="grid"))
    print("a. Sob a suposição não-paramétrica\nb. Hipótese nula: área verdadeira = 0.5")
    
    
def plot_roc_curve_with_best_threshold(model, data_train, dependent_var):

    """
    Plota a curva ROC, calcula o melhor threshold (Youden Index), exibe a AUC e destaca o melhor ponto com coordenadas.

    Parâmetros:
    - model: Modelo treinado com método predict_proba() ou predict().
    - data_train: DataFrame contendo os dados de treino, incluindo a variável dependente.
    - dependent_var: Nome da variável dependente (target) no DataFrame.

    Retorno:
    - Exibe a curva ROC e tabela com informações sobre o melhor threshold.
    """

    # Separa X_train (features) e y_train (target)
    X_train = data_train.drop(columns=[dependent_var])
    y_train = data_train[dependent_var]

    # Verifica se o modelo tem predict_proba() ou apenas predict()
    if hasattr(model, "predict_proba"):
        y_pred_probs = model.predict_proba(X_train)[:, 1]  # Probabilidade da classe positiva
    else:
        y_pred_probs = model.predict(X_train)  # Usa predição binária diretamente

    # Calcula curva ROC
    fpr, tpr, thresholds = roc_curve(y_train, y_pred_probs)
    roc_auc_value = auc(fpr, tpr)

    # Verifica se há classes suficientes
    n1, n2 = np.sum(y_train == 1), np.sum(y_train == 0)
    if n1 == 0 or n2 == 0:
        raise ValueError("Classes positivas e negativas não podem estar vazias.")

    # Índice de Youden (TPR - FPR) -> Melhor threshold
    youden_index = tpr + (1 - fpr) - 1
    best_idx = np.argmax(youden_index)
    best_threshold = thresholds[best_idx]
    best_fpr, best_tpr = fpr[best_idx], tpr[best_idx]

    # Gráfico da Curva ROC usando Plotly com coordenadas do melhor ponto
    fig = go.Figure()

    # Curva ROC
    fig.add_trace(go.Scatter(
        x=fpr, y=tpr,
        mode='lines', name=f'AUC = {roc_auc_value:.3f}',
        line=dict(color='blue', width=2)
    ))

    # Melhor Ponto com Coordenadas (Threshold Ótimo)
    fig.add_trace(go.Scatter(
        x=[best_fpr], y=[best_tpr],
        mode='markers+text',
        name=f'Threshold Youden = {best_threshold:.3f}',
        marker=dict(color='red', size=10),
        text=[f"({best_fpr:.3f}, {best_tpr:.3f})"],
        textposition="top center"
    ))

    # Linha de referência (Modelo Aleatório)
    fig.add_trace(go.Scatter(
        x=[0, 1], y=[0, 1],
        mode='lines', name='Modelo Aleatório',
        line=dict(dash='dash', color='gray')
    ))

    # Ajustes do layout do gráfico
    fig.update_layout(
        title="Curva ROC (TREINO)",
        xaxis_title="1 - Especificidade (FPR)",
        yaxis_title="Sensibilidade (TPR)",
        width=700,
        height=600,
        showlegend=True
    )

    # Exibe o gráfico
    fig.show()
    

def auc_performance_comparison(modelo, data_train, data_test, dependent_var, random_state=42, 
                               n_bootstraps=1000, multi_class='ovr', average='macro'):
    """
    Avalia a performance de um modelo de classificação para dados multiclasse, 
    comparando o AUC-ROC entre os conjuntos de treino e teste. Opcionalmente, 
    utiliza reamostragem via bootstrap para estimar o erro padrão, intervalos de confiança e p-valores.
    
    Parâmetros:
    - modelo: modelo treinado (que possua o método `.predict` retornando probabilidades).
    - data_train (pd.DataFrame): Conjunto de treino.
    - data_test (pd.DataFrame): Conjunto de teste.
    - dependent_var (str): Nome da variável dependente.
    - random_state (int): Semente para reprodução dos resultados. Padrão: 42.
    - multi_class (str): Método para cálculo do AUC em problemas multiclasse. Padrão: "ovr".
    - average (str): Tipo de média para cálculo do AUC em problemas multiclasse. Padrão: "macro".
    - n_bootstraps (int): Número de reamostragens para o bootstrap. Padrão: 1000.
        
    Retorna:
    - Imprime uma tabela comparativa do AUC-ROC entre treino e teste.
    """
    
    # Obter as probabilidades preditas
    train_pred_probs = modelo.predict(data_train)
    test_pred_probs = modelo.predict(data_test)
    
    # Extrair as classes reais
    y_train = data_train[dependent_var].values
    y_test = data_test[dependent_var].values

    # Cálculo dos AUCs base
    try:
        auc_train = roc_auc_score(y_train, train_pred_probs, multi_class=multi_class, average=average)
        auc_test = roc_auc_score(y_test, test_pred_probs, multi_class=multi_class, average=average)
    except ValueError:
        return "Erro: Impossível calcular AUC devido à ausência de alguma classe no conjunto de dados."
    
    # Função interna para cálculo do AUC via bootstrap
    def bootstrap_auc(y_true, pred_probs, n_bootstraps, random_seed):
        rng = np.random.RandomState(random_seed)
        bootstrapped_scores = []
        n = len(y_true)

        for _ in range(n_bootstraps):
            indices = rng.randint(0, n, n)
            y_boot = y_true[indices]
            # Compatibiliza com DataFrame ou array numpy
            if hasattr(pred_probs, 'iloc'):
                p_boot = pred_probs.iloc[indices].to_numpy()
            else:
                p_boot = pred_probs[indices]

            try:
                score = roc_auc_score(y_boot, p_boot, multi_class=multi_class, average=average)
                bootstrapped_scores.append(score)
            except ValueError:
                continue  # Ignora amostras em que alguma classe desaparece

        if len(bootstrapped_scores) < 2:
            return np.nan, np.nan, np.nan, np.nan

        auc_array = np.array(bootstrapped_scores)
        auc_mean = auc_array.mean()
        se_auc = auc_array.std(ddof=1)  # erro padrão amostral

        # Intervalo de Confiança de 95%
        z975 = norm.ppf(0.975)
        ci_lower = auc_mean - z975 * se_auc
        ci_upper = auc_mean + z975 * se_auc

        return auc_mean, se_auc, ci_lower, ci_upper

    # Estimação via bootstrap para treino e teste
    auc_train_mean, se_train, lower_train, upper_train = bootstrap_auc(y_train, train_pred_probs, n_bootstraps, random_state)
    auc_test_mean, se_test, lower_test, upper_test = bootstrap_auc(y_test, test_pred_probs, n_bootstraps, random_state)

    # Cálculo dos p-valores para H0: AUC = 0.5
    p_value_train = 2 * (1 - norm.cdf(abs((auc_train - 0.5) / se_train))) if not np.isnan(se_train) else np.nan
    p_value_test = 2 * (1 - norm.cdf(abs((auc_test - 0.5) / se_test))) if not np.isnan(se_test) else np.nan

    # Diferença entre treino e teste
    diff_auc = auc_train - auc_test
    se_diff = np.sqrt(se_train**2 + se_test**2) if (not np.isnan(se_train) and not np.isnan(se_test)) else np.nan
    p_diff = 2 * (1 - norm.cdf(abs(diff_auc / se_diff))) if not np.isnan(se_diff) else np.nan
    z_crit = norm.ppf(0.975)
    diff_lower = diff_auc - z_crit * se_diff if not np.isnan(se_diff) else np.nan
    diff_upper = diff_auc + z_crit * se_diff if not np.isnan(se_diff) else np.nan

    # Preparação e impressão da tabela com resultados do bootstrap
    rows_auc = [
        ["Treino", f"{auc_train:.3f}", f"{se_train:.3f}", f"{p_value_train:.3f}", f"{lower_train:.3f}", f"{upper_train:.3f}"],
        ["Teste", f"{auc_test:.3f}", f"{se_test:.3f}", f"{p_value_test:.3f}", f"{lower_test:.3f}", f"{upper_test:.3f}"],
        ["Treino - Teste", f"{diff_auc:.3f}", f"{se_diff:.3f}", f"{p_diff:.3f}", f"{diff_lower:.3f}", f"{diff_upper:.3f}"]
    ]

    print("\n=== COMPARAÇÃO DE AUC-ROC COM BOOTSTRAPPING (TRAIN VS. TEST) ===")
    print(tabulate(rows_auc, headers=["Amostra", "AUC", "Erro Padrão", "p-Valor", "IC 95% Inf", "IC 95% Sup"], tablefmt="grid"))
 
        
def stepwise_selection(
    data,
    dependent_var,
    independent_numerical_vars,
    independent_categorical_vars,
    p_value_stepwise_threshold=0.05,
    stepwise_method='backward',
    include_intercept=True,
    model_type='binary',
    verbose=False
):

    # Gera todos os termos a partir dos preditores
    all_terms = generate_terms(independent_numerical_vars, independent_categorical_vars)
    
    # Se houver apenas um preditor disponível, retorna-o imediatamente
    if len(all_terms) == 1:
        if verbose:
            print("Apenas um preditor disponível. Retornando-o como modelo final.")
        return all_terms
    
    
    if stepwise_method not in ['backward', 'forward']:
        raise ValueError("O parâmetro 'stepwise_method' deve ser 'backward' ou 'forward'.")
    
    if stepwise_method == 'backward':
        temp_terms = generate_terms(independent_numerical_vars, independent_categorical_vars)
    else:
        temp_terms = []
        remaining_terms = generate_terms(independent_numerical_vars, independent_categorical_vars)
              
    while True:
        if verbose:
            print("\nVariáveis no modelo:", temp_terms)
        
        # Criação da fórmula e ajuste do modelo
        temp_formula = build_formula(dependent_var, independent_numerical_vars, independent_categorical_vars, temp_terms, include_intercept, 'plain')        
        modelo_ajustado = fit_model(temp_formula, data, model_type)
        
        if verbose:
            print("Fórmula do modelo atual:", temp_formula)
            print(modelo_ajustado.summary())

        # Obtém os p-valores dos coeficientes (exceto intercepto)
        pvals = modelo_ajustado.pvalues.drop(labels='Intercept', errors='ignore')
        
        if verbose:
            print("p-valores:", pvals)

        if stepwise_method == 'backward':
            
            # Verifica se pvals é um DataFrame
            if isinstance(pvals, pd.Series):
                # Se for uma Series, converte para DataFrame
                pvals = pvals.to_frame()
        
            # Calcula o pior p‑valor para cada preditor (maior p‑valor entre os outcomes)
            worst_p_values = pvals.max(axis=1)

            # Identifica o preditor com o maior p‑valor (o "pior" preditor)
            worst_term = worst_p_values.idxmax()
            worst_p_value = worst_p_values.max()

            if worst_p_value <= p_value_stepwise_threshold:
                break

            if verbose:
                print(f"Removendo '{worst_term}' (p={worst_p_value:.4f})")

            temp_terms.remove(worst_term)
        
        elif stepwise_method == 'forward':
            best_p_value = float('inf')
            best_term = None
            
            for term in remaining_terms:
                test_terms = temp_terms + [term]
                test_formula = build_formula(dependent_var, independent_numerical_vars, independent_categorical_vars, test_terms, include_intercept, 'plain')
                test_model = fit_model(test_formula, data, model_type)
                
                test_pvals = test_model.pvalues.drop(labels='Intercept', errors='ignore')
                
                if term in test_pvals and test_pvals[term] < p_value_stepwise_threshold and test_pvals[term] < best_p_value:
                    best_p_value = test_pvals[term]
                    best_term = term
            
            if best_term is None:
                break  # Nenhum termo pode ser adicionado com p < p_value_stepwise_threshold
            
            temp_terms.append(best_term)
            remaining_terms.remove(best_term)
            
            if verbose:
                print(f"Adicionando '{best_term}' (p={best_p_value:.4f})")
    
    return temp_terms

def fit_model(formula, data, model_type='multinomial'):
    """
    Ajusta um modelo de regressão logística com base no tipo especificado.

    Parâmetros:
    ------------
    formula : str
        Fórmula estatística no estilo R, ex: 'y ~ x1 + x2'.
    data : pd.DataFrame
        DataFrame contendo os dados.
    model_type : str, opcional (default='multinomial')
        Tipo do modelo a ser ajustado. Opções disponíveis:
          - 'binary'      => Regressão logística binária (`sm.Logit`).
          - 'multinomial' => Regressão logística multinomial (`sm.MNLogit`).
          - 'ordinal'     => Regressão logística ordinal (`OrderedModel`).

    Retorna:
    --------
    model_fitted : statsmodels model
        Modelo ajustado, que pode ser uma instância de:
          - `sm.Logit` (logística binária),
          - `sm.MNLogit` (logística multinomial),
          - `OrderedModel` (logística ordinal).

    Levanta:
    --------
    ValueError:
        Se `model_type` não for uma das opções válidas ('binary', 'multinomial' ou 'ordinal').

    Exemplo de uso:
    --------------
    ```python
    import pandas as pd
    from statsmodels.formula.api import logit

    df = pd.DataFrame({'y': [0, 1, 1, 0], 'x1': [2.3, 1.5, 3.1, 4.2]})
    model = fit_model('y ~ x1', data=df, model_type='binary')
    print(model.summary())
    ```
    """

    model_type = model_type.lower()  # Padroniza entrada

    # === MODELO ORDINAL ===
    if model_type == 'ordinal':
        import patsy
        # Cria as matrizes de resposta (y) e preditoras (X) usando Patsy
        y, X = patsy.dmatrices(formula, data, return_type='dataframe')
        y = y.squeeze()  # Garante que y seja uma Series se for uma única coluna

        # Remove coluna de intercepto, se existir
        for const_name in ['Intercept', 'const']:
            if const_name in X.columns:
                X = X.drop(columns=const_name)

        # Se não houver preditores, cria uma coluna dummy de zeros
        if X.shape[1] == 0:
            X = pd.DataFrame(
                np.zeros((data.shape[0], 1)),
                index=data.index,
                columns=['dummy']
            )

        mod = OrderedModel(endog=y, exog=X, distr='logit')
        model_fitted = mod.fit(method='lbfgs', disp=False)
        # Armazena a matriz de desenho usada no ajuste
        model_fitted.model.data.orig_exog = X.copy()

        return model_fitted

    # === REGRESSÃO LOGÍSTICA BINÁRIA ===
    elif model_type == 'binary':
        try:
            # Tenta ajustar o modelo normalmente
            model_fitted = smf.logit(formula, data=data).fit(disp=False)
        except np.linalg.LinAlgError as err:
            if "Singular matrix" in str(err):
                model_fitted = smf.logit(formula, data=data).fit_regularized(disp=False)
            else:
                raise  # Relevanta outros erros que não sejam de matriz singular
        return model_fitted

    # === REGRESSÃO LOGÍSTICA MULTINOMIAL ===
    elif model_type == 'multinomial':
        model_fitted = smf.mnlogit(formula, data=data).fit(disp=False)
        return model_fitted

    else:
        raise ValueError(f"Tipo de modelo inválido: '{model_type}'. Escolha entre 'binary', 'multinomial' ou 'ordinal'.")
    

def converter_categoria_baseline(df, col_resp, baseline_value=None):
    """
    Converte a coluna de resposta de um DataFrame para códigos [0, 1, ..., k-1],
    atribuindo o código 0 à categoria baseline (referência) especificada.
    
    Parâmetros
    ----------
    df : pandas.DataFrame
        DataFrame que contém a coluna de resposta.
    col_resp : str
        Nome da coluna de resposta a ser convertida.
    baseline_value : int ou None, opcional
        Valor da categoria que deverá ser considerado como baseline (código 0).
        Se None, utiliza a ordem natural dos valores únicos.
    
    Retorna
    -------
    df : pandas.DataFrame
        DataFrame com uma nova coluna (col_resp + "_code") contendo os códigos [0..k-1].
    cat_map : dict
        Dicionário de mapeamento original -> novo código.

    """
    # Garante que a coluna de resposta seja do tipo inteiro
    df[col_resp] = df[col_resp].astype(int)
    
    # Obtém os valores únicos e ordenados da coluna de resposta
    original_cats = np.sort(df[col_resp].unique())
    
    # Se baseline_value for especificado, reordena as categorias
    if baseline_value is not None:
        if baseline_value not in original_cats:
            raise ValueError(
                f"Valor '{baseline_value}' não existe em df['{col_resp}']. "
                f"Categorias encontradas: {list(original_cats)}"
            )
        # Coloca a categoria baseline na primeira posição e o restante depois
        new_order = [baseline_value] + [x for x in original_cats if x != baseline_value]
    else:
        new_order = list(original_cats)
    
    # Cria um dicionário de mapeamento: categoria original -> novo código
    cat_map = {val: i for i, val in enumerate(new_order)}
    
    # Cria uma nova coluna com os códigos mapeados
    col_resp_code = col_resp + "_code"
    df[col_resp_code] = df[col_resp].map(cat_map)
    
    return df, col_resp_code


def plot_logits_V11022025(
    df, 
    modelo_final, 
    dependent_var,                # coluna com as categorias (ex.: 1, 2, 3)
    independent_vars         # pode ser string (única) ou lista de strings
):
    """
    Plota subplots de log(p_A / p_B) em função de uma ou mais variáveis explicativas,
    considerando todos os pares de categorias da variável dependente.
    
    Parâmetros
    ----------
    df : pd.DataFrame
        DataFrame que contém as colunas necessárias (incluindo dependent_var e independent_vars).
    modelo_final : objeto statsmodels MNLogit (ou similar)
        Modelo multinomial já ajustado, com método .predict().
    dependent_var : str
        Nome da coluna com as categorias dependentes (ex.: "Chá").
    independent_vars : str ou list de str
        Nome(s) da(s) coluna(s) usada(s) como eixo X (ex.: "Disposição" ou ["Disposição", "OutraVar"]).
        
    Retorna
    -------
    Exibe o gráfico interativo (Plotly) contendo os subplots.
    """
    # 1) Se independent_vars for string, converte para lista
    if isinstance(independent_vars, str):
        independent_vars_list = [independent_vars]
    else:
        independent_vars_list = independent_vars

    # 2) Identifica as categorias únicas na coluna dependent_var
    df_temp = df.copy()
    unique_cats = np.sort(df_temp[dependent_var].unique().astype(int))
    # Ex.: [1, 2, 3] ou [0, 1, 2], etc.

    # 3) Gera todas as combinações 2 a 2 de categorias
    pairs = list(combinations(unique_cats, 2))

    n_rows = len(independent_vars_list)
    n_cols = len(pairs)

    # 4) Cria títulos para cada subplot
    subplot_titles = []
    for var in independent_vars_list:
        for (a, b) in pairs:
            subplot_titles.append(f"{var}: log(p_{a}/p_{b})")

    # 5) Prepara a figura com subplots (grade: rows x cols)
    fig = make_subplots(rows=n_rows, cols=n_cols, subplot_titles=subplot_titles)

    # 6) Loop principal: para cada variável explicativa (linha) e para cada par de categorias (coluna)
    for i, var in enumerate(independent_vars_list, start=1):

        # Ordena o DataFrame pela variável explicativa
        df_sorted = df_temp.sort_values(by=var).copy()

        # Obtém as probabilidades previstas
        predicted_probs = modelo_final.predict(df_sorted)
        model_cols = np.sort(predicted_probs.columns)

        # Se o número de colunas em predicted_probs bater com o número de categorias únicas,
        # cria um mapeamento para renomear as colunas, igualando-as às categorias do DF.
        if len(model_cols) == len(unique_cats):
            map_dict = {mc: uc for mc, uc in zip(model_cols, unique_cats)}
            predicted_probs = predicted_probs.rename(columns=map_dict)
        else:
            print("[AVISO] Nº de colunas em predicted_probs difere do nº de categorias em dependent_var.")
            print("        Pode ser que exista baseline interna ou outra codificação no modelo.")
            print(f"        Colunas do modelo: {model_cols}")
            print(f"        Categorias em {dependent_var}: {unique_cats}")

        for j, (catA, catB) in enumerate(pairs, start=1):
            x_vals = df_sorted[var]
            pA = predicted_probs[catA]
            pB = predicted_probs[catB]

            # Calcula log(pA / pB), evitando log(0)
            logit = np.log(pA.replace(0, np.nan) / pB.replace(0, np.nan))

            # a) Plot dos pontos
            fig.add_trace(
                go.Scatter(
                    x=x_vals,
                    y=logit,
                    mode='markers',
                    name=f"Logit({catA}/{catB}) - {var}",
                    showlegend=False  # Para não repetir a legenda em cada subplot
                ),
                row=i, col=j
            )

            # b) Ajuste de regressão linear (exemplo)
            #    (Cuidado com casos sem pontos ou NaN)
            valid_mask = ~logit.isna()
            if valid_mask.sum() > 1:
                coefs = np.polyfit(x_vals[valid_mask], logit[valid_mask], 1)  # grau 1 => reta
                poly = np.poly1d(coefs)
                y_fit = poly(x_vals)

                # R² simples
                ss_res = np.sum((logit[valid_mask] - y_fit[valid_mask])**2)
                ss_tot = np.sum((logit[valid_mask] - np.mean(logit[valid_mask]))**2)
                r2 = 1 - ss_res / ss_tot if ss_tot != 0 else 0

                # Plota a reta
                fig.add_trace(
                    go.Scatter(
                        x=x_vals,
                        y=y_fit,
                        mode='lines',
                        name=f"Reg lin ({catA}/{catB}) - {var}",
                        showlegend=False
                    ),
                    row=i, col=j
                )

                # c) Anotação da equação + R²
                slope = coefs[0]
                intercept = coefs[1]
                eq_text = (
                    f"y = {intercept:.2f} + {slope:.2f}*x<br>"
                    f"R² = {r2:.2f}"
                )

                x_median = x_vals.median()
                y_median = np.median(logit.dropna())
                fig.add_annotation(
                    x=x_median,
                    y=y_median,
                    text=eq_text,
                    showarrow=True,
                    arrowhead=2,
                    row=i, col=j
                )
            else:
                # Se houver poucos ou nenhum ponto válido para regressão
                fig.add_annotation(
                    x=0.5,
                    y=0.5,
                    text="Poucos dados ou NaNs para regressão",
                    showarrow=False,
                    xref="x domain",
                    yref="y domain",
                    row=i, col=j
                )

            # Ajusta eixos
            fig.update_xaxes(title_text=var, row=i, col=j)
            fig.update_yaxes(title_text=f"log(p_{catA}/p_{catB})", row=i, col=j)

    # 7) Layout final
    big_title = f"Logits de {dependent_var}"

    # Ajusta o tamanho da figura de acordo com o número de subplots
    fig_width = 300 * n_cols
    fig_height = 400 * n_rows

    fig.update_layout(
        width=fig_width,
        height=fig_height,
        title=big_title
    )

    return fig.show()

def plot_logits(
    df,
    modelo_final,
    dependent_var,
    independent_numerical_vars,
    independent_categorical_vars,
    invert_logit=True
):
    """
    Plota subplots de log(p_A / p_B) (ou log(p_B / p_A), se invert_logit=True) 
    em função de uma ou mais variáveis explicativas.

    Parâmetros
    ----------
    df : pd.DataFrame
        Conjunto de dados.
    modelo_final : objeto statsmodels (Logit, MNLogit, OrderedModel, etc.)
        Modelo já ajustado, com método .predict() disponível.
    dependent_var : str
        Nome da coluna com as categorias dependentes (ex.: "Chá", "Emprestimo", etc.).
    independent_numerical_vars : list de str
        Nomes das colunas numéricas para plotar no eixo X.
    independent_categorical_vars : list de str
        Nomes das colunas categóricas para plotar no eixo X.
    invert_logit : bool
        Se True, faz log(p_B / p_A) em vez de log(p_A / p_B).

    Retorna
    -------
    Exibe um gráfico Plotly com subplots (linhas = variáveis explicativas, colunas = pares de categorias).
    """

    # Combina as variáveis numéricas e categóricas
    independent_vars_list = list(independent_numerical_vars) + list(independent_categorical_vars)

    if len(independent_vars_list) == 0:
        print("Nenhuma variável independente fornecida.")
        return

    df_temp = df.copy()
    unique_cats = np.sort(df_temp[dependent_var].unique().astype(int))
    pairs = list(combinations(unique_cats, 2))

    n_rows = len(independent_vars_list)
    n_cols = len(pairs)

    # Títulos para cada subplot
    subplot_titles = []
    for var in independent_vars_list:
        for (a, b) in pairs:
            if not invert_logit:
                subplot_titles.append(f"{var}: log(p_{a}/p_{b})")
            else:
                subplot_titles.append(f"{var}: log(p_{b}/p_{a})")

    fig = make_subplots(rows=n_rows, cols=n_cols, subplot_titles=subplot_titles)

    for i, var in enumerate(independent_vars_list, start=1):
        is_numeric = var in independent_numerical_vars

        # Ordena se numérica
        if is_numeric:
            df_sorted = df_temp.sort_values(by=var).copy()
        else:
            df_sorted = df_temp.copy()

        # Obtém previsões e padroniza
        predicted_probs = modelo_final.predict(df_sorted)
        predicted_probs = _adjust_prediction_format(predicted_probs, df_sorted, dependent_var)

        for j, (catA, catB) in enumerate(pairs, start=1):
            x_vals = df_sorted[var]
            pA = predicted_probs[catA]
            pB = predicted_probs[catB]

            # Logit = log(pA/pB) ou log(pB/pA), dependendo de invert_logit
            if invert_logit:
                logit_vals = np.log(pB.replace(0, np.nan) / pA.replace(0, np.nan))
            else:
                logit_vals = np.log(pA.replace(0, np.nan) / pB.replace(0, np.nan))

            # Plot dos pontos
            fig.add_trace(
                go.Scatter(
                    x=x_vals,
                    y=logit_vals,
                    mode='markers',
                    name=f"Logit({catA}/{catB}) - {var}",
                    showlegend=False
                ),
                row=i, col=j
            )

            # Se numérica, tenta ajuste linear
            if is_numeric:
                valid_mask = ~logit_vals.isna()
                if valid_mask.sum() > 1:
                    coefs = np.polyfit(x_vals[valid_mask], logit_vals[valid_mask], 1)
                    poly = np.poly1d(coefs)
                    y_fit = poly(x_vals)

                    # R²
                    ss_res = np.sum((logit_vals[valid_mask] - y_fit[valid_mask])**2)
                    ss_tot = np.sum((logit_vals[valid_mask] - np.mean(logit_vals[valid_mask]))**2)
                    r2 = 1 - ss_res / ss_tot if ss_tot != 0 else 0

                    fig.add_trace(
                        go.Scatter(
                            x=x_vals,
                            y=y_fit,
                            mode='lines',
                            name=f"Reg lin ({catA}/{catB}) - {var}",
                            showlegend=False
                        ),
                        row=i, col=j
                    )

                    # Equação + R²
                    slope, intercept = coefs
                    eq_text = (
                        f"y = {intercept:.2f} + {slope:.2f}*x<br>"
                        f"R² = {r2:.2f}"
                    )
                    x_median = x_vals.median()
                    y_median = np.median(logit_vals.dropna())
                    fig.add_annotation(
                        x=x_median,
                        y=y_median,
                        text=eq_text,
                        showarrow=True,
                        arrowhead=2,
                        row=i, col=j
                    )
                else:
                    fig.add_annotation(
                        x=0.5,
                        y=0.5,
                        text="Poucos dados ou NaNs para regressão",
                        showarrow=False,
                        xref="x domain",
                        yref="y domain",
                        row=i, col=j
                    )
            else:
                # Categórica, não faz regressão linear
                fig.add_annotation(
                    x=0.5,
                    y=0.5,
                    text="Não aplicável regressão para variável categórica",
                    showarrow=False,
                    xref="x domain",
                    yref="y domain",
                    row=i, col=j
                )

            # Ajustes de eixos
            fig.update_xaxes(title_text=var, row=i, col=j)
            if invert_logit:
                fig.update_yaxes(title_text=f"log(p_{catB}/p_{catA})", row=i, col=j)
            else:
                fig.update_yaxes(title_text=f"log(p_{catA}/p_{catB})", row=i, col=j)

    big_title = f"Logits de {dependent_var}"
    fig_width = 300 * n_cols
    fig_height = 400 * n_rows

    fig.update_layout(
        width=fig_width,
        height=fig_height,
        title=big_title
    )

    fig.show()


def _adjust_prediction_format(predicted_probs, df_sorted, dependent_var):
    """
    Função auxiliar para padronizar a saída de .predict() em um DataFrame
    com colunas representando cada categoria da variável dependente.
    Suporta modelos binários, multinomiais e ordinais.
    """
    df_temp = df_sorted.copy()
    unique_cats = np.sort(df_temp[dependent_var].unique().astype(int))

    # Se for Series (comum em binário)
    if isinstance(predicted_probs, pd.Series):
        if len(unique_cats) == 2:
            # A Series representa a prob da classe 'positiva'
            predicted_probs = pd.DataFrame({
                unique_cats[0]: 1 - predicted_probs,
                unique_cats[1]: predicted_probs
            }, index=df_temp.index)
        else:
            raise ValueError(
                "O modelo retornou uma Series, mas há mais de 2 categorias na variável dependente."
            )
    elif isinstance(predicted_probs, np.ndarray):
        predicted_probs = pd.DataFrame(predicted_probs, index=df_temp.index)

    # Se DataFrame, tenta renomear colunas conforme as categorias encontradas
    if isinstance(predicted_probs, pd.DataFrame):
        # Tenta converter as colunas para int (se ainda não estiverem)
        try:
            predicted_probs.columns = predicted_probs.columns.astype(int)
        except:
            pass

        model_cols = np.sort(predicted_probs.columns)
        if len(model_cols) == len(unique_cats):
            map_dict = {mc: uc for mc, uc in zip(model_cols, unique_cats)}
            predicted_probs = predicted_probs.rename(columns=map_dict)
        else:
            print("[AVISO] Número de colunas em predicted_probs difere do número de categorias em dependent_var.")
            print("       Pode haver baseline interna ou outra codificação no modelo.")
            print(f"       Colunas do modelo: {model_cols}")
            print(f"       Categorias em {dependent_var}: {unique_cats}")
    else:
        raise ValueError("Formato de saída de 'predict' não reconhecido. Espera-se Series, np.ndarray ou DataFrame.")

    return predicted_probs



def _adjust_prediction_format(predicted_probs, df_sorted, dependent_var):
    """
    Função auxiliar para padronizar a saída de .predict() em um DataFrame
    com colunas representando cada categoria da variável dependente.
    Suporta modelos binários, multinomiais e ordinais.
    """
    df_temp = df_sorted.copy()
    unique_cats = np.sort(df_temp[dependent_var].unique().astype(int))

    # Se for Series (comum em binário)
    if isinstance(predicted_probs, pd.Series):
        if len(unique_cats) == 2:
            # A Series representa a prob da classe 'positiva'
            predicted_probs = pd.DataFrame({
                unique_cats[0]: 1 - predicted_probs,
                unique_cats[1]: predicted_probs
            }, index=df_temp.index)
        else:
            raise ValueError(
                "O modelo retornou uma Series, mas há mais de 2 categorias na variável dependente."
            )
    elif isinstance(predicted_probs, np.ndarray):
        predicted_probs = pd.DataFrame(predicted_probs, index=df_temp.index)

    # Se DataFrame, tenta renomear colunas conforme as categorias encontradas
    if isinstance(predicted_probs, pd.DataFrame):
        # Tenta converter as colunas para int (se ainda não estiverem)
        try:
            predicted_probs.columns = predicted_probs.columns.astype(int)
        except:
            pass

        model_cols = np.sort(predicted_probs.columns)
        if len(model_cols) == len(unique_cats):
            map_dict = {mc: uc for mc, uc in zip(model_cols, unique_cats)}
            predicted_probs = predicted_probs.rename(columns=map_dict)
        else:
            print("[AVISO] Número de colunas em predicted_probs difere do número de categorias em dependent_var.")
            print("       Pode haver baseline interna ou outra codificação no modelo.")
            print(f"       Colunas do modelo: {model_cols}")
            print(f"       Categorias em {dependent_var}: {unique_cats}")
    else:
        raise ValueError("Formato de saída de 'predict' não reconhecido. Espera-se Series, np.ndarray ou DataFrame.")

    return predicted_probs




def plot_predicted_probabilities_OLD(df, model, independent_vars):
    """
    Plota as probabilidades previstas de um modelo de regressão logística
    (binária, multinomial ou ordinal) para uma ou mais variáveis explicativas.

    Parâmetros
    ----------
    df : pd.DataFrame
        DataFrame contendo as variáveis do modelo.
    model : statsmodels Logit / MNLogit / OrderedModel
        Modelo de regressão já ajustado.
    independent_vars : str ou list de str
        Nome(s) da(s) variável(is) independente(s) que será(ão) o eixo X.
    """
    if isinstance(independent_vars, str):
        independent_vars = [independent_vars]

    # Paleta de cores padrão
    palette = qualitative.Plotly
    
    # Obtém previsões de probabilidades
    predicted_probs = model.predict(df)
    categorias = predicted_probs.columns if isinstance(predicted_probs, pd.DataFrame) else [0, 1]
    
    # Mapeamento de cores para categorias
    cat_color_map = {cat: palette[i % len(palette)] for i, cat in enumerate(categorias)}
    
    for var in independent_vars:
        df_sorted = df.sort_values(by=var)
        predicted_probs_sorted = model.predict(df_sorted)
        
        fig = go.Figure()
        for cat in categorias:
            fig.add_trace(
                go.Scatter(
                    x=df_sorted[var],
                    y=predicted_probs_sorted[cat] if isinstance(predicted_probs_sorted, pd.DataFrame) else predicted_probs_sorted,
                    mode='lines',
                    name=f"Prob Cat {cat}",
                    line=dict(color=cat_color_map[cat])
                )
            )
        
        fig.update_layout(
            title=""f"Probabilidades Previstas vs {var}""",
            xaxis_title=var,
            yaxis_title="Probabilidades Previstas"
        )
        
        fig.show()


def plot_predicted_probabilities(
    df,
    modelo_final,
    dependent_var,
    independent_numerical_vars,
    independent_categorical_vars
):
    """
    Plota as probabilidades preditas para cada categoria da variável dependente
    em função das variáveis independentes (numéricas e categóricas).

    Parâmetros
    ----------
    df : pd.DataFrame
        Conjunto de dados (incluindo dependent_var e as variáveis independentes).
    modelo_final : objeto statsmodels (Logit, MNLogit, OrderedModel, etc.)
        Modelo já ajustado, com método .predict() disponível.
    dependent_var : str
        Nome da coluna com as categorias dependentes.
    independent_numerical_vars : list de str
        Nomes das colunas numéricas para plotar.
    independent_categorical_vars : list de str
        Nomes das colunas categóricas para plotar.

    Retorna
    -------
    Exibe um gráfico Plotly com subplots (linhas = variáveis, colunas = categorias).
    """

    # Combina as variáveis
    independent_vars_list = list(independent_numerical_vars) + list(independent_categorical_vars)
    if len(independent_vars_list) == 0:
        print("Nenhuma variável independente fornecida.")
        return

    df_temp = df.copy()
    unique_cats = np.sort(df_temp[dependent_var].unique().astype(int))
    n_rows = len(independent_vars_list)
    n_cols = len(unique_cats)

    # Títulos dos subplots
    subplot_titles = []
    for var in independent_vars_list:
        for cat in unique_cats:
            subplot_titles.append(f"{var} - p(Cat={cat})")

    fig = make_subplots(rows=n_rows, cols=n_cols, subplot_titles=subplot_titles)

    # Loop por variável (linha)
    for i, var in enumerate(independent_vars_list, start=1):
        is_numeric = var in independent_numerical_vars

        if is_numeric:
            df_sorted = df_temp.sort_values(by=var).copy()
        else:
            df_sorted = df_temp.copy()

        # Calcula probabilidades e padroniza em DF
        predicted_probs = modelo_final.predict(df_sorted)
        predicted_probs = _adjust_prediction_format(predicted_probs, df_sorted, dependent_var)

        # Loop por categoria dependente (coluna)
        for j, cat in enumerate(unique_cats, start=1):
            if is_numeric:
                # Para variável numérica, plotamos linha vs x
                x_vals = df_sorted[var]
                y_vals = predicted_probs[cat]

                fig.add_trace(
                    go.Scatter(
                        x=x_vals,
                        y=y_vals,
                        mode='lines+markers',
                        name=f"p({cat}) vs {var}",
                        showlegend=False
                    ),
                    row=i, col=j
                )
                fig.update_xaxes(title_text=var, row=i, col=j)
                fig.update_yaxes(title_text=f"p(cat={cat})", row=i, col=j)

            else:
                # Para variável categórica, calculamos a média da probabilidade
                # por cada nível da variável
                grouped = (
                    df_sorted
                    .groupby(var)
                    .apply(lambda g: predicted_probs.loc[g.index, cat].mean(), include_groups=False)
                )

                x_vals = grouped.index.astype(str)
                y_vals = grouped.values

                # Plotamos como barras
                fig.add_trace(
                    go.Bar(
                        x=x_vals,
                        y=y_vals,
                        name=f"p({cat}) vs {var}",
                        showlegend=False
                    ),
                    row=i, col=j
                )
                fig.update_xaxes(title_text=var, row=i, col=j)
                fig.update_yaxes(title_text=f"p(cat={cat})", row=i, col=j)

    big_title = f"Probabilidades Preditas de {dependent_var}"
    fig_width = 300 * n_cols
    fig_height = 400 * n_rows

    fig.update_layout(
        width=fig_width,
        height=fig_height,
        title=big_title
    )

    fig.show()


def classification_report(model, X_test, y_true_test, dependent_var, classification_threshold=0.5):
    """
    Avalia um modelo de regressão logística binária, multinomial ou ordinal.

    Parâmetros:
      - model: modelo treinado (deve possuir os métodos predict e, se disponível, predict_proba)
      - X_test: DataFrame contendo as variáveis preditoras do conjunto de teste
      - y_true_test: Série ou array com os valores reais da variável dependente
      - dependent_var: Nome da variável dependente (apenas para referência na saída)
      - classification_threshold: valor de corte para classificação binária (padrão = 0.5)

    Retorno:
      - Imprime a matriz de confusão e métricas de desempenho formatadas.
    """

    # Garante que y_true_test seja um array de inteiros
    y_true_test = np.array(y_true_test, dtype=int)

    # Realiza as previsões no conjunto de teste
    if hasattr(model, "predict_proba"):
        test_pred_probs = model.predict_proba(X_test)
        class_labels = model.classes_
        
        # Para problema binário, aplica o classification_threshold à probabilidade da classe positiva
        if len(class_labels) == 2:
            y_pred_test = (test_pred_probs[:, 1] >= classification_threshold).astype(int)
        else:
            # Para multiclasse, seleciona a classe com maior probabilidade
            y_pred_test = np.array([class_labels[i] for i in np.argmax(test_pred_probs, axis=1)], dtype=int)
    else:
        # Para modelos que não possuem o método predict_proba (ex.: alguns do statsmodels)
        y_pred_probs = model.predict(X_test)
        if y_pred_probs.ndim == 1:
            y_pred_test = (y_pred_probs >= classification_threshold).astype(int)
        else:
            y_pred_test = np.array(np.argmax(y_pred_probs, axis=1), dtype=int)

    # Obtém todas as classes presentes nos dados
    classes_test = sorted(list(set(y_true_test) | set(y_pred_test)))
    
    # Calcula a matriz de confusão
    cmat_test = confusion_matrix(y_true_test, y_pred_test, labels=classes_test)

    # Imprime a matriz de confusão formatada
    print("\n=== MATRIZ DE CONFUSÃO ===")
    headers_test = ["Real\\Pred"] + [str(c) for c in classes_test] + ["Total"]
    rows_test = []
    for i, c_real in enumerate(classes_test):
        row = [str(c_real)] + list(cmat_test[i, :]) + [cmat_test[i, :].sum()]
        rows_test.append(row)
    col_sum_test = cmat_test.sum(axis=0)
    rows_test.append(["Total"] + list(col_sum_test) + [col_sum_test.sum()])
    print(tabulate(rows_test, headers=headers_test, tablefmt="grid"))
    
    # Calcula as métricas de desempenho
    accuracy = accuracy_score(y_true_test, y_pred_test)
    precision = precision_score(y_true_test, y_pred_test, average="weighted", zero_division=0)
    recall = recall_score(y_true_test, y_pred_test, average="weighted", zero_division=0)
    f1 = f1_score(y_true_test, y_pred_test, average="weighted", zero_division=0)

    # Cria o dicionário com as métricas (excluindo a especificidade, caso não seja binário)
    metrics = {
         "Acurácia": accuracy,
         "Precisão": precision,
         "Sensibilidade (Recall)": recall,
         "F1-Score": f1
    }

    # Se o problema for binário, calcula e adiciona a especificidade
    if len(classes_test) == 2:
         tn, fp, fn, tp = cmat_test.ravel()
         specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
         metrics["Especificidade"] = specificity

    # Formata as métricas para que os valores numéricos tenham três casas decimais
    formatted_metrics = [
         (metric, f"{value:.3f}" if isinstance(value, (int, float)) else value)
         for metric, value in metrics.items()
    ]

    # Imprime a tabela de métricas
    print("\n=== MÉTRICAS DE DESEMPENHO ===")
    print(tabulate(formatted_metrics, headers=["Métrica", "Valor"], tablefmt="grid"))


def predict_for_rows(model, dep_var, data, rows):
    """
    Função genérica para prever linhas específicas de um DataFrame,
    reconstruindo apenas as colunas realmente necessárias (slopes) para o modelo ordinal.
    """
    selected_data = data.iloc[rows].copy()
    if dep_var in selected_data.columns:  # Ajuste para sua dep_var real
        selected_data.drop(columns=[dep_var], inplace=True)
    
    exog_names = model.model.exog_names
    exog = pd.DataFrame(index=selected_data.index)
    
    for col_name in exog_names:
        if "/" in col_name:
            continue
        if col_name.startswith("C("):
            var_part = col_name.split("]")[0].replace("C(", "")
            var_name, cat_value = var_part.split("[T.")
            var_name = var_name.strip(")")
            cat_value = cat_value.strip()
            exog[col_name] = (selected_data[var_name].astype(str) == cat_value).astype(float)
        else:
            exog[col_name] = selected_data[col_name]
    
    preds = model.predict(exog)
    return preds

def predict_specific_instance(model, instance_dict):
    """
    Realiza previsão para um caso específico fornecido via dicionário.
    """
    instance_df = pd.DataFrame([instance_dict])
    
    try:
        dep_var = model.model.data.orig_endog_names
        if isinstance(dep_var, list):
            dep_var = dep_var[0]
        if dep_var in instance_df.columns:
            instance_df = instance_df.drop(columns=[dep_var])
    except Exception:
        pass
    
    try:
        design_info = model.model.data.design_info
        exog = design_info.transform(instance_df)
        expected_names = model.model.data.exog_names
        exog = exog[expected_names]
    except AttributeError:
        try:
            expected_cols = model.model.data.orig_exog.columns.tolist()
            exog = instance_df[expected_cols].copy()
        except Exception:
            exog = instance_df.copy()
    
    predictions = model.predict(exog)
    return predictions


def logistic_regression_analysis(
    data,
    dependent_var,
    independent_numerical_vars=[],
    independent_categorical_vars=[],
    model_type='multinomial',   # "binary", "multinomial", "ordinal"
    baseline_category=None,
    include_intercept=True,
    data_split=True, test_size=0.2, random_state=42,
    show_model_summary_to_intercept_only=True,
    show_model_summary_to_saturated=True,
    show_model_summary_to_stepwise=False, stepwise_method='backward', p_value_stepwise_threshold=0.05,
    show_odds_summary=False,
    show_goodness_of_fit=False,
    show_plot_logits=False,
    show_plot_predicted_probabilities=False,
    show_plot_odds_ratio_increments=False,
    show_classification_report=False, classification_threshold=0.5,
    show_auc_roc_report=True,
    show_auc_performance_comparison=True,
    prediction_rows=None,              # NOVO: indices específicos para previsão
    specific_prediction=None,           # NOVO: dicionário com previsão específica
    verbose=False
):

    data = data.copy()
    # Convertendo dependent_var para inteiros, para execução mais robusta
    data[dependent_var] = data[dependent_var].astype(int)
    
    if model_type == 'multinomial':
        data, dependent_var = converter_categoria_baseline(data, dependent_var, baseline_category)
    
    # Separando dados de treino e teste
    if data_split:
        data_train, data_test = split_dataset(data, test_size, random_state)
        X_train, y_train = data_train.drop(columns=[dependent_var]), data_train[dependent_var]
        X_test, y_true_test = data_test.drop(columns=[dependent_var]), data_test[dependent_var] 
    else:
        data_train, data_test = data, data
        X_train, y_train = data_train.drop(columns=[dependent_var]), data_train[dependent_var]
        X_test, y_true_test = data_test.drop(columns=[dependent_var]), data_test[dependent_var]
    
    # Preditores para fins de Goodness of Fitness (GOF)
    predictors_intercept_only = []
    predictors_saturated = generate_terms(independent_numerical_vars, independent_categorical_vars)
    predictors_stepwise = stepwise_selection(data_train,
                                             dependent_var,
                                             independent_numerical_vars,
                                             independent_categorical_vars,
                                             p_value_stepwise_threshold,
                                             stepwise_method,
                                             include_intercept,
                                             model_type,
                                             False)

    # Fórmulas
    formula_intercept_only = build_formula(dependent_var, independent_numerical_vars, independent_categorical_vars, predictors_intercept_only, include_intercept, 'patsy')
    formula_saturated = build_formula(dependent_var, independent_numerical_vars, independent_categorical_vars, predictors_saturated, include_intercept, 'patsy')
    formula_stepwise = build_formula(dependent_var, independent_numerical_vars, independent_categorical_vars, predictors_stepwise, include_intercept, 'patsy')
    
    # Modelos
    modelo_intercept_only = fit_model(formula_intercept_only, data_train, model_type)
    modelo_saturated = fit_model(formula_saturated, data_train, model_type)
    modelo_stepwise = fit_model(formula_stepwise, data_train, model_type)
    
    # Exibindo Modelos   
    if show_model_summary_to_intercept_only:
        print("\n=== MODELO INTERCEPTO (TRAIN DATA) ===")
        print(modelo_intercept_only.summary())
    
    if show_model_summary_to_saturated:
        print("\n=== MODELO SATURADO (TRAIN DATA) ===")
        print(modelo_saturated.summary())    
    
    if show_model_summary_to_stepwise:
        print("\n=== MODELO STEPWISE (TRAIN DATA) ===")
        print(modelo_stepwise.summary())
    
    if show_odds_summary:
        logistic_regression_odds_summary(modelo_stepwise, model_type)
        
    if show_goodness_of_fit:
        goodness_of_fit(modelo_intercept_only, modelo_saturated, modelo_stepwise)
        
    if show_plot_logits:
        plot_logits(data, modelo_stepwise, dependent_var, independent_numerical_vars, independent_categorical_vars)
        
    if show_plot_predicted_probabilities:
        plot_predicted_probabilities(data, modelo_stepwise, dependent_var, independent_numerical_vars, independent_categorical_vars)
    
    if show_plot_odds_ratio_increments:
        plot_odds_ratio_increments(data, modelo_stepwise, 
                                    dependent_var, independent_numerical_vars, independent_categorical_vars,
                                    increment_steps=10, max_increment=100)
        
    if show_classification_report:
        classification_report(modelo_stepwise, X_test, y_true_test, dependent_var, classification_threshold)
        
    if show_auc_roc_report:
        plot_roc_curve_with_best_threshold(modelo_stepwise, data_train, dependent_var)
        auc_roc_table(modelo_stepwise, data_train, dependent_var)
        
    if show_auc_performance_comparison:
        auc_performance_comparison(modelo_stepwise, data_train, data_test, dependent_var, random_state)
        
    if prediction_rows is not None:
        print("\n=== PREDICTIONS FOR SPECIFIC ROWS ===")
        preds_rows = predict_for_rows(modelo_stepwise, dependent_var, data, prediction_rows)
        print(preds_rows)
        
    if specific_prediction is not None:
        print("\n=== PREDICTION FOR SPECIFIC INPUT ===")
        preds_specific = predict_specific_instance(modelo_stepwise, specific_prediction)
        print(preds_specific)
    