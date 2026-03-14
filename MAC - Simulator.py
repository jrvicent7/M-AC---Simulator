import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox
import math
import cmath
import numpy as np
import sys
import os
from PIL import Image


# Função para carregar imagem dentro do app
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def opcao_selecionada(selecionado):
    global ax1
    # entrada_selecionada = pop_input_data.get()
    #"Com Dados de Ensaio"
    btn_clear.place(relwidth=0.1, relheight=0.1, relx=0.87, rely=0.87)


    if selecionado == "Com Dados do MIT":
        ax1 = fig_MIT.add_subplot(1, 1, 1)
        canvas_MIT.draw()
        
        #COM DADOS DO MIT
        pop_rotor_type.configure(state="normal")
        pop_graphs.configure(state="normal")
        input_polos.configure(state="normal")
        input_Vlinha.configure(state="normal")
        input_f.configure(state="normal")
        input_R1.configure(state="normal")
        input_R2.configure(state="normal")
        input_X1.configure(state="normal")
        input_X2.configure(state="normal")
        input_Xm.configure(state="normal")
        input_s.configure(state="normal")
        input_Pvent.configure(state="normal")
        input_Pnuc.configure(state="normal")
        btn_simular_curva.place(relwidth=0.3, relheight=0.1, relx=0.56, rely=0.87)

        # COM DADOS DE ENSAIO
        pop_category.configure(state="disabled")
        input_Vcc.configure(state="disabled")
        input_Icc.configure(state="disabled")
        input_Vt_vz.configure(state="disabled")
        input_Il_vz.configure(state="disabled")
        input_frequency_vz.configure(state="disabled")
        input_Pin_vz.configure(state="disabled")
        input_Vt_rb.configure(state="disabled")
        input_Il_rb.configure(state="disabled")
        input_frequency_rb.configure(state="disabled")
        input_Pin_rb.configure(state="disabled")
        btn_calcular_circuito.place_forget()
        label_circuito_MIT.place_forget()
        txt_output_R1.place_forget()
        output_R1.place_forget()
        txt_output_X1.place_forget()
        output_X1.place_forget()
        txt_output_R2.place_forget()
        output_R2.place_forget()
        txt_output_X2.place_forget()
        output_X2.place_forget()
        txt_output_Xm.place_forget()
        output_Xm.place_forget()
    
    else:
        fig_MIT.clear()
        canvas_MIT.draw() 

        #COM DADOS DO MIT
        pop_rotor_type.configure(state="disabled")
        pop_graphs.configure(state="disabled")
        input_polos.configure(state="disabled")
        input_Vlinha.configure(state="disabled")
        input_f.configure(state="disabled")
        input_R1.configure(state="disabled")
        input_R2.configure(state="disabled")
        input_X1.configure(state="disabled")
        input_X2.configure(state="disabled")
        input_Xm.configure(state="disabled")
        input_s.configure(state="disabled")
        input_Pvent.configure(state="disabled")
        input_Pnuc.configure(state="disabled")
        btn_simular_curva.place_forget()

        # COM DADOS DE ENSAIO
        pop_category.configure(state="normal")
        input_Vcc.configure(state="normal")
        input_Icc.configure(state="normal")
        input_Vt_vz.configure(state="normal")
        input_Il_vz.configure(state="normal")
        input_frequency_vz.configure(state="normal")
        input_Pin_vz.configure(state="normal")
        input_Vt_rb.configure(state="normal")
        input_Il_rb.configure(state="normal")
        input_frequency_rb.configure(state="normal")
        input_Pin_rb.configure(state="normal")
        btn_calcular_circuito.place(relwidth=0.3, relheight=0.1, relx=0.56, rely=0.87)
        label_circuito_MIT.place(x=995, y=65)  # Coordenadas absolutas
        txt_output_R1.place(relwidth=0.032, relheight=0.04, relx=0.71, rely=0.2)
        output_R1.place(relwidth=0.032, relheight=0.04, relx=0.71, rely=0.24)
        txt_output_X1.place(relwidth=0.032, relheight=0.04, relx=0.635, rely=0.2)
        output_X1.place(relwidth=0.032, relheight=0.04, relx=0.635, rely=0.24)
        txt_output_R2.place(relwidth=0.032, relheight=0.04, relx=0.9, rely=0.395)
        output_R2.place(relwidth=0.032, relheight=0.04, relx=0.9, rely=0.435)
        txt_output_X2.place(relwidth=0.032, relheight=0.04, relx=0.886, rely=0.2)
        output_X2.place(relwidth=0.032, relheight=0.04, relx=0.886, rely=0.24)
        txt_output_Xm.place(relwidth=0.032, relheight=0.04, relx=0.73, rely=0.395)
        output_Xm.place(relwidth=0.032, relheight=0.04, relx=0.73, rely=0.435)
        

def plot_Graphical():
    global ax1
    global Flag_rotor
    global Flag_graph

    inputs = [input_polos, input_Vlinha, input_f, input_R1, input_R2, input_X1, 
              input_X2, input_Xm, input_s, input_Pvent, input_Pnuc]

    valores = []

    #Verificação de números negativos e letras

    for entry in inputs:
        valor = entry.get().strip()
        
        # Se estiver vazio, adiciona None ou 0 e continua
        if not valor:
            valores.append(0)  # ou valores.append(0)
            continue
        
        try:
            numero = float(valor)
            
            # Verifica se é maior ou igual a zero
            if numero < 0:
                messagebox.showerror("Erro", "Insira apenas números positivos.")
                entry.delete(0, 'end')
                entry.focus()
                return
            
            valores.append(numero)

        except ValueError:
            messagebox.showerror("Erro", "Insira apenas números positivos.")
            entry.delete(0, 'end')
            entry.focus()
            return
    
    polos, Vslinha, fs, R1, R2, X1, X2, Xm, snom, PAeV, Pnuc = valores

    # VALIDAÇÃO: Evitar divisão por zero
    if polos == 0:
        messagebox.showerror("Erro", "Número de polos deve ser maior que zero!")
        return
    
    if fs == 0:
        messagebox.showerror("Erro", "Frequência deve ser maior que zero!")
        return
    
    if snom == 0:
        messagebox.showerror("Erro", "Escorregamento nominal deve ser maior que zero!")
        return

    #EQUIVALENTE DE THEVENNIN

    ns=(120*fs)/polos # Velocidade síncrona
    omegas = ((math.pi)/30)*ns # Velocidade síncrona em rad/s
    Vs = Vslinha/(math.sqrt(3)) # Tensão de fase da alimentação do estator

    # --- Cálculo da Impedância de Thevennin ---

    Zth = ((R1+1j*X1)*(1j*Xm))/((R1+1j*X1)+(1j*Xm)); # Impedância de Thevennin
    Rth = Zth.real
    Xth = Zth.imag

    #Calculando a tensao do equivalente de Thevenin 
    Vth = Vs*((1j*Xm)/(R1+1j*(X1+Xm))) # Tensão de Thévenin
    Vthabs = abs(Vth) # |Vth| -> módulo/valor absoluto de Vth

    # CALCULO DOS RESULTADOS

    # CONJUGADO MÁXIMO
    Tmax = (3*(Vthabs**2))/((2*omegas)*(Rth+(math.sqrt(Rth**2+((Xth+X2)**2))))) # Torque Máximo
    output_Tmax.configure(state="normal")
    output_Tmax.delete(0, 'end') # Limpa o valor anterior
    output_Tmax.insert(0, f"{Tmax:.2f}") # Insere o valor de Tmáx
    output_Tmax.configure(state="readonly")

    # VELOCIDADE NO CONJUGADO MÁXIMO
    smax = R2/math.sqrt((Rth**2)+((Xth+X2)**2)) # Calcula o valor do escorregamento p/ Tmáx
    NmTmax = (1-smax)*ns # Calcula velocidade de Tmáx
    output_Vel_Tmax.configure(state="normal")
    output_Vel_Tmax.delete(0, 'end') # Limpa o valor anterior
    output_Vel_Tmax.insert(0, f"{NmTmax:.2f}") # Insere o valor da Velocidade em Torque máximo
    output_Vel_Tmax.configure(state="readonly")

    # CONJUGADO DE PARTIDA
    Tpartida = (1/omegas)*((3*(Vthabs**2)*(R2))/((Rth+(R2))**2+(Xth+X2)**2)) # Calcula o conjugado de partida
    output_Tpart.configure(state="normal")
    output_Tpart.delete(0, 'end') # Limpa o valor anterior
    output_Tpart.insert(0, f"{Tpartida:.2f}") # Insere o valor do Conjugado de Partida
    output_Tpart.configure(state="readonly")

    # VELOCIDADE NOMINAL
    nm = ((1-(snom/100)))*ns # Velocidade Nominal
    output_Vel_Nom.configure(state="normal")
    output_Vel_Nom.delete(0, 'end') # Limpa o valor anterior
    output_Vel_Nom.insert(0, f"{nm:.1f}") # Insere o valor de Nm
    output_Vel_Nom.configure(state="readonly")

    # POTÊNCIA DE ENTRADA
    snominal = snom / 100
    Z1 = R1 + 1j*X1
    Z2 = R2/snominal + 1j*X2
    Zf = ((1j*Xm) * Z2) / ((1j*Xm) + Z2)
    Ztot = Z1 + Zf
    Ia = Vs / Ztot

    # Conversão polar (módulo e ângulo)
    Ro = abs(Ia)  # Módulo
    Theta = cmath.phase(Ia)  # Ângulo em radianos

    Ilabs = abs(Ia)

    Pin = math.sqrt(3) * Vslinha * Ilabs * math.cos(Theta)
    Pinabs = abs(Pin)
    output_Pin.configure(state="normal")
    output_Pin.delete(0, 'end') # Limpa o valor anterior
    output_Pin.insert(0, f"{Pinabs:.0f}") # Insere o valor da Potência de Entrada
    output_Pin.configure(state="readonly")

    # PERDAS NO COBRE DO ESTATOR
    PCE = 3*(Ilabs**2)*R1
    output_PCE.configure(state="normal")
    output_PCE.delete(0, 'end') # Limpa o valor anterior
    output_PCE.insert(0, f"{PCE:.2f}") # Insere o valor da Perda no Cobre do Estator
    output_PCE.configure(state="readonly")

    # POTÊNCIA DE ENTREFERRO
    PEF = Pinabs-PCE-Pnuc
    output_PEF.configure(state="normal")
    output_PEF.delete(0, 'end') # Limpa o valor anterior
    output_PEF.insert(0, f"{PEF:.0f}") # Insere o valor da Perda no Entreferro
    output_PEF.configure(state="readonly")

    # POTÊNCIA CONVERTIDA
    Pconv = (1-snominal)*PEF
    output_Pconv.configure(state="normal")
    output_Pconv.delete(0, 'end') # Limpa o valor anterior
    output_Pconv.insert(0, f"{Pconv:.0f}") # Insere o valor da Potência Convertida
    output_Pconv.configure(state="readonly")

    # POTÊNCIA DE SAÍDA
    Pout = Pconv-PAeV
    output_Pout.configure(state="normal")
    output_Pout.delete(0, 'end') # Limpa o valor anterior
    output_Pout.insert(0, f"{Pout:.0f}") # Insere o valor da Potência de Saída
    output_Pout.configure(state="readonly")
        
    # CONJUGADO INDUZIDO
    Tind = (PEF/omegas)
    output_Tind.configure(state="normal")
    output_Tind.delete(0, 'end') # Limpa o valor anterior
    output_Tind.insert(0, f"{Tind:.2f}") # Insere o valor do Conjugado Induzido
    output_Tind.configure(state="readonly")

    # CONJUGADO DE SAÍDA
    omegam = ((1-snominal)*omegas)
    Tout = (Pout/omegam)
    output_Tout.configure(state="normal")
    output_Tout.delete(0, 'end') # Limpa o valor anterior
    output_Tout.insert(0, f"{Tout:.2f}") # Insere o valor do Conjugado de Saída
    output_Tout.configure(state="readonly")

    # EFICIÊNCIA
    eficiencia = ((Pout/Pinabs)*100)
    output_Efic.configure(state="normal")
    output_Efic.delete(0, 'end') # Limpa o valor anterior
    output_Efic.insert(0, f"{eficiencia:.2f}") # Insere o valor da Eficiência
    output_Efic.configure(state="readonly")

    # CORRENTE NOMINAL
    Inomabs = abs(Ia)
    output_I_Nom.configure(state="normal")
    output_I_Nom.delete(0, 'end') # Limpa o valor anterior
    output_I_Nom.insert(0, f"{Inomabs:.2f}") # Insere o valor da Corrente Nominal
    output_I_Nom.configure(state="readonly")

    # CORRENTE DE PARTIDA
    Z1 = R1 + 1j*X1
    Z2 = R2/1 + 1j*X2
    Zf = ((1j*Xm) * Z2)/((1j*Xm) + Z2)
    Ztot = Z1 + Zf
    Ipart = Vs/Ztot
    Ipartabs = abs(Ipart)
    output_I_Part.configure(state="normal")
    output_I_Part.delete(0, 'end') # Limpa o valor anterior
    output_I_Part.insert(0, f"{Ipartabs:.2f}") # Insere o valor da Corrente de Partida
    output_I_Part.configure(state="readonly")

    # CURVA CARACTERÍSTICA E CORRENTE
    s_values = np.arange(1, 0.001, -0.0005)
    
    # Velocidade do rotor
    n = ns * (1 - s_values)
    
    # Torque eletromagnético
    Tem = (1/omegas) * ((3 * Vthabs**2 * (R2/s_values)) / ((Rth + R2/s_values)**2 + (Xth + X2)**2))

    
    # Corrente
    Z1 = R1 + 1j*X1
    Z2 = R2/s_values + 1j*X2
    Zf = (1j*Xm * Z2) / (1j*Xm + Z2)
    Zeq = Z1 + Zf
    Is = Vs / Zeq
    Isabs = np.abs(Is)

    rotor_selecionado = pop_rotor_type.get()
    grafico_selecionado = pop_graphs.get()

    if rotor_selecionado == "Gaiola de Esquilo":

        Flag_rotor = 0

        # Limpar o gráfico anterior
        fig_MIT.clear()

        ax1 = fig_MIT.add_subplot(1, 1, 1)

        if grafico_selecionado == "Conjugado X Velocidade":
            
            # GRÁFICO 1: Torque x Velocidade
            ax1.plot(n, Tem, 'b-', linewidth=2, label='Torque Eletromagnético')
            ax1.set_xlabel('Velocidade (rpm)', fontsize=12, fontweight='bold')
            ax1.set_ylabel('Torque (N.m)', fontsize=12, fontweight='bold')
            ax1.set_title('Conjugado x Velocidade', fontsize=14, fontweight='bold')
            ax1.grid(True, alpha=0.3)
            ax1.legend()

            # Marcar pontos importantes no gráfico de torque
            ax1.plot(NmTmax, Tmax, 'ro', markersize=8, label=f'Tmáx = {Tmax:.2f} N.m')
            ax1.plot(0, Tpartida, 'go', markersize=8, label=f'Tpart = {Tpartida:.2f} N.m')
            ax1.legend()

        
        elif grafico_selecionado == "Corrente X Velocidade":

            # ax1 = fig_MIT.add_subplot(1, 1, 1)

            # GRÁFICO 2: Corrente x Velocidade
            ax1.plot(n, Isabs, 'r-', linewidth=2, label='Corrente do Estator')
            ax1.set_xlabel('Velocidade (rpm)', fontsize=12, fontweight='bold')
            ax1.set_ylabel('Corrente (A)', fontsize=12, fontweight='bold')
            ax1.set_title('Corrente x Velocidade', fontsize=14, fontweight='bold')
            ax1.grid(True, alpha=0.3)
            ax1.legend()
            
            # Marcar pontos importantes no gráfico de corrente
            ax1.plot(0, Ipartabs, 'go', markersize=8, label=f'Ipart = {Ipartabs:.2f} A')
            ax1.plot(nm, Inomabs, 'mo', markersize=8, label=f'Inom = {Inomabs:.2f} A')
            ax1.legend()
    

    elif rotor_selecionado == "Bobinado":

        if Flag_rotor == 0:
                fig_MIT.clear()
                ax1 = fig_MIT.add_subplot(1, 1, 1)
                Flag_rotor += 1
    

        if grafico_selecionado == "Conjugado X Velocidade":
            
            if Flag_graph == 0:
                fig_MIT.clear()
                ax1 = fig_MIT.add_subplot(1, 1, 1)
                Flag_graph += 1
            
            # GRÁFICO 1: Torque x Velocidade
            ax1.plot(n, Tem, 'b-', linewidth=2, 
                    #  label='Torque Eletromagnético',
                     )
            ax1.set_xlabel('Velocidade (rpm)', fontsize=12, fontweight='bold')
            ax1.set_ylabel('Torque (N.m)', fontsize=12, fontweight='bold')
            ax1.set_title('Conjugado x Velocidade', fontsize=14, fontweight='bold')
            ax1.grid(True, alpha=0.3)
            # ax1.legend()

            # Marcar pontos importantes no gráfico de torque
            # ax1.plot(NmTmax, Tmax, 'ro', markersize=8, label=f'Tmáx = {Tmax:.2f} N.m')
            # ax1.plot(0, Tpartida, 'go', markersize=8, label=f'Tpart = {Tpartida:.2f} N.m')
            ax1.legend()

        
        elif grafico_selecionado == "Corrente X Velocidade":

            if Flag_graph == 1:
                fig_MIT.clear()
                ax1 = fig_MIT.add_subplot(1, 1, 1)
                Flag_graph -= 1

            # ax1 = fig_MIT.add_subplot(1, 1, 1)

            # GRÁFICO 2: Corrente x Velocidade
            ax1.plot(n, Isabs, 'r-', linewidth=2, 
                    #  label='Corrente do Estator'
                     )
            ax1.set_xlabel('Velocidade (rpm)', fontsize=12, fontweight='bold')
            ax1.set_ylabel('Corrente (A)', fontsize=12, fontweight='bold')
            ax1.set_title('Corrente x Velocidade', fontsize=14, fontweight='bold')
            ax1.grid(True, alpha=0.3)
            ax1.legend()
            
            # Marcar pontos importantes no gráfico de corrente
            # ax1.plot(0, Ipartabs, 'go', markersize=8, label=f'Ipart = {Ipartabs:.2f} A')
            # ax1.plot(nm, Inomabs, 'mo', markersize=8, label=f'Inom = {Inomabs:.2f} A')
            # ax1.legend()

    # Atualizar o canvas
    canvas_MIT.draw()


def calculate_circuit():

    inputs = [input_Vcc, input_Icc, input_Vt_vz, input_Il_vz, input_frequency_vz, 
              input_Pin_vz, input_Vt_rb, input_Il_rb, input_frequency_rb, input_Pin_rb]

    valores = []

    #Verificação de númros negativos e letras

    for entry in inputs:
        valor = entry.get().strip()
        
        # Se estiver vazio, adiciona None ou 0 e continua
        if not valor:
            valores.append(0)  # ou valores.append(0)
            continue
        
        try:
            numero = float(valor)
            
            # Verifica se é maior ou igual a zero
            if numero < 0:
                messagebox.showerror("Erro", "Insira apenas números positivos.")
                entry.delete(0, 'end')
                entry.focus()
                return
            
            valores.append(numero)

        except ValueError:
            messagebox.showerror("Erro", "Insira apenas números positivos.")
            entry.delete(0, 'end')
            entry.focus()
            return
        
    Vcc, Icc, Vtv, Ilv, fv, Pinv, Vtrb, Ilrb, frb, Pinrb = valores

     # Cálculo de R1 com dados do ensaio CC
    R1 = Vcc / (2 * Icc)
    
    # Cálculo da Impedância a Vazio
    Vfv = Vtv / math.sqrt(3)  # Tensão de Fase a Vazio
    
    # Portanto...
    Zv = Vfv / Ilv  # Impedância da Máquina a Vazio ≈ X1 + Xm
    
    # Cálculo das perdas à Vazio
    Pcev = 3 * (Ilv**2) * R1  # Perdas no Cobre do Estator a Vazio
    Prot = Pinv - Pcev  # Perdas Rotacionais a Vazio
    
    # Cálculos do Ensaio Rotor Bloqueado
    Vfrb = Vtrb / math.sqrt(3)  # Tensão de Fase c/ Rotor Bloqueado
    
    # Portanto...
    Zrb = Vfrb / Ilrb  # Impedância da Máquina c/ Rotor Bloqueado
    
    # Ângulo de Impedância
    theta = math.acos(Pinrb / (math.sqrt(3) * Vtrb * Ilrb))
    
    Rrb = math.cos(theta) * Zrb  # Resistência c/ Rotor Bloqueado
    
    # Portanto
    R2 = Rrb - R1  # Determinação da Resistência R2
    
    # Reatância em 15Hz
    Xrb15 = Zrb * math.sin(theta)
    
    # Reatância em 60Hz
    Xrb60 = (60 / 15) * Xrb15

    categoria = pop_category.get()

    if categoria == "Categoria N":
        X2 = Xrb60/1.68
        X1 = Xrb60-X2

    if categoria == "Categoria H":
        X2 = Xrb60/1.58
        X1 = Xrb60-X2  
    
    if categoria == "Categoria D":
        X2 = Xrb60/1.78
        X1 = Xrb60-X2

    Xm = Zv - X1

    # RESISTÊNCIA DO ESTATOR
    output_R1.configure(state="normal")
    output_R1.delete(0, 'end') # Limpa o valor anterior
    output_R1.insert(0, f"{R1:.3f}") # Insere o valor da Potência de Saída
    output_R1.configure(state="readonly")

    # REATÂNCIA DO ESTATOR
    output_X1.configure(state="normal")
    output_X1.delete(0, 'end') # Limpa o valor anterior
    output_X1.insert(0, f"{X1:.3f}") # Insere o valor da Potência de Saída
    output_X1.configure(state="readonly")

    # RESISTÊNCIA DO ROTOR
    output_R2.configure(state="normal")
    output_R2.delete(0, 'end') # Limpa o valor anterior
    output_R2.insert(0, f"{R2:.3f}") # Insere o valor da Potência de Saída
    output_R2.configure(state="readonly")

    # REATÂNCIA DO ROTOR
    output_X2.configure(state="normal")
    output_X2.delete(0, 'end') # Limpa o valor anterior
    output_X2.insert(0, f"{X2:.3f}") # Insere o valor da Potência de Saída
    output_X2.configure(state="readonly")

    # REATÂNCIA DE MAGNETIZAÇÃO
    output_Xm.configure(state="normal")
    output_Xm.delete(0, 'end') # Limpa o valor anterior
    output_Xm.insert(0, f"{Xm:.3f}") # Insere o valor da Potência de Saída
    output_Xm.configure(state="readonly")


def plot_V_curve():
    global msinc_values
    global resposta
    global flag_grafico_1
    global contador_de_fasores
    global contador_de_motores

    inputs = [input_Vfase, input_polos_msinc, input_f_msinc, input_Pot_acionada_msinc, 
              input_FP_msinc, input_Xs_msinc, input_If_msinc, input_Prot_msinc, input_Pnuc_msinc]

    valores = []

    #Verificação de númros negativos e letras

    for entry in inputs:
        valor = entry.get().strip()
        
        # Se estiver vazio, adiciona None ou 0 e continua
        if not valor:
            valores.append(0)  # ou valores.append(0)
            continue
        
        try:
            numero = float(valor)
            
            # Verifica se é maior ou igual a zero
            if numero < 0:
                messagebox.showerror("Erro", "Insira apenas números positivos.")
                entry.delete(0, 'end')
                entry.focus()
                return
            
            valores.append(numero)

        except ValueError:
            messagebox.showerror("Erro", "Insira apenas números positivos.")
            entry.delete(0, 'end')
            entry.focus()
            return
        
    Vfase, polos, f, Pot_acionada_HP, FP, Xs, If_inicial, Prot, Pnuc = valores
    
    Pot_acionada = Pot_acionada_HP*746
    FP_unitario = 1

    status_FP = status_FP_sgmtd.get()

    Pin = Pot_acionada + Prot + Pnuc

    magnitud_Ia = Pin / (3 * Vfase * FP)

    if status_FP == "Atrasado":
        Ia1 = cmath.rect(magnitud_Ia, -math.acos(FP))

    else:    
        Ia1 = cmath.rect(magnitud_Ia, math.acos(FP)) 

    angulo_Ia = math.degrees(cmath.phase(Ia1))

    Ea1 = Vfase - 1j*Xs*Ia1
    angulo_Ea1 = math.degrees(cmath.phase(Ea1))
    delta1 = angulo_Ea1 * math.pi / 180  # delta1 em radianos - (Ângulo de Carga)

    XsIa = 1j*Xs*Ia1
    angulo_XsIa = math.degrees(cmath.phase(XsIa))

    #Calcula o valor de Ia quando FP = 1
    magnitud_Ia_fp_unitario = Pin / (3 * Vfase * FP_unitario) 
    Ia_fp_unitario = cmath.rect(magnitud_Ia_fp_unitario, -math.acos(FP_unitario))

    #Calcula o valor de Ea quando FP = 1
    Ea_FP_unitario = Vfase - 1j*Xs*Ia_fp_unitario
    angulo_Ea1_FP_unitario = math.degrees(cmath.phase(Ea_FP_unitario))

    #Calcula o valor de If quando FP = 1
    If_FP_unitario = (abs(Ea_FP_unitario)*If_inicial)/abs(Ea1) # Relação - Ea1 / If

    # Defini os limites da curva
    If_max = If_FP_unitario + 1.1 # Ponto Máx de If depois de FP = 1
    If_min = If_FP_unitario - 1 # Ponto Mín de If depois de FP = 1

    If = np.arange(If_min, If_max, 0.01) # Cria uma variação de If indo de If_min até If_máx definido anteriormente a um passo de 0.01

    Ea_2 = (If*abs(Ea1)) / If_inicial # Calcula cada valor que Ea pode assumir dentro da variação de If (de If_min a If_max)

    # delta2 = np.arcsin(abs(Ea1) / abs(Ea_2) * math.sin(delta1)) # Calcula todos os Ângulos de Carga para cada valor de Ea_2 (de If_min a If_max)

    ratio = np.clip(abs(Ea1) / abs(Ea_2) * math.sin(delta1), -1, 1)
    delta2 = np.arcsin(ratio)
    
    Ea = Ea_2 * np.exp(1j * -delta2) # Cria uma array com todos os fasores Ea (de If_min a If_max)

    Ia = (Vfase-Ea) / (1j*Xs) # Cria uma array com todos os fasores Ia (de If_min a If_max)

    def plotar_grafico_unico():
        global valores_limites
        global cores_Ea
        global cores_Ia
        global cores_XsIa
        global contador_de_fasores

        # GRÁFICO 2: If x Ia
        ax2.plot(If, abs(Ia), linewidth=2, label=f'Máq. {contador_de_motores} | Pout = {Pot_acionada/746:.1f} HP | If = {If_inicial} A')
        ax2.set_xlabel('Corrente de Campo, A', fontsize=12, fontweight='bold')
        
        ax2.set_ylabel('Corrente de Armadura, A', fontsize=12, fontweight='bold')
        ax2.set_xticks(np.arange(int(min(If))-1.5, int(max(If)) + 1.5, 0.25))
        ax2.set_yticks(range(int(abs(Ia_fp_unitario))-1, int(max(abs(Ia))) + 1, 1))
        ax2.set_title('Corrente de Campo x Corrente de Armadura', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.legend()

        idx = contador_de_fasores % len(cores_Ea)

        # Marcar pontos importantes no gráfico de corrente
        ax2.plot(If_FP_unitario, abs(Ia_fp_unitario), marker='o', markersize=8, color=cores_marcador_FP1[idx], label=f'FP = 1 | If = {abs(If_FP_unitario):.2f} A | Ia = {abs(Ia_fp_unitario):.2f} A')
        ax2.plot(If_inicial, abs(Ia1), markersize=8, marker='o', color=cores_marcador_If[idx], label=f'If = {If_inicial} | Ia = {abs(Ia1):.2f} A')
        ax2.legend()

        # Fasores
        fasor = contador_de_fasores * "'"

        # Plotar múltiplos vetores
        # Fasor Ea
        ax3.arrow(0, 0, Ea1.real, Ea1.imag,
                head_width=7, head_length=8,
                fc=cores_Ea[idx], ec=cores_Ea[idx],
                lw=2.5,
                length_includes_head=True, alpha=0.7,
                label=f'Ea{fasor} {abs(Ea1):.2f} ∠{angulo_Ea1:.2f}°')
        
        # Fasor Ia
        ax3.arrow(0, 0, Ia1.real, Ia1.imag,
                head_width=5, head_length=6,
                fc=cores_Ia[idx], ec=cores_Ia[idx],
                lw=2.5,
                length_includes_head=True, alpha=0.7,
                label=f'Ia{fasor} {abs(Ia1):.2f} ∠{angulo_Ia:.2f}°')
        
        # Fasor queda de Tensão XsIa
        ax3.arrow(Ea1.real, Ea1.imag, XsIa.real, XsIa.imag,
                head_width=5, head_length=6,
                fc=cores_XsIa[idx], ec=cores_XsIa[idx],
                lw=2.5,
                length_includes_head=True, alpha=0.7,
                label=f'XsIa{fasor} {abs(XsIa):.2f} ∠{angulo_XsIa:.2f}°')
        
        # Fasor tensão de Fase
        ax3.arrow(0, 0, Vfase, 0,
                head_width=5, head_length=6,
                fc='green', ec='green',
                lw=2.5,
                length_includes_head=True, alpha=0.7,
                label=f'Vφ{fasor} {Vfase:.2f} ∠{0}°')
        
        # Lista com todos os vetores
        valores_limites.extend([abs(Ea1.real), abs(Ea1.imag),
                               abs(Ia1.real), abs(Ia1.imag),
                               abs(XsIa.real), abs(XsIa.imag),
                               Vfase])
        
        max_val = max(valores_limites)  # Encontra o maior valor entre todos os vetores
        
        # Configurar limites
        ax3.set_xlim(-max_val*0.3, max_val*1.3)
        ax3.set_ylim(-max_val, max_val)

        # ✅ Remover os números dos eixos
        ax3.set_xticks([])
        ax3.set_yticks([])

        ax3.set_xlabel('Real', fontsize=12, fontweight='bold')
        ax3.set_ylabel('Imaginário', fontsize=12, fontweight='bold')
        ax3.set_title('Diagrama Fasorial', fontsize=14, fontweight='bold')
        ax3.grid(True, alpha=0.3)
        ax3.axhline(0, color='black', linewidth=0.8)
        ax3.axvline(0, color='black', linewidth=0.8)
        # ax3.set_aspect('equal')
        ax3.legend()

        contador_de_fasores += 1


    def plotar_multigraficos():
        global flag_grafico_1
        global valores_limites
        global contador_de_fasores
        global cores_Ea
        global cores_Ia
        global cores_XsIa
        
         
        if flag_grafico_1 == 0: # É o primeiro gráfico?
            plotar_grafico_unico()
            msinc_values.append([If_inicial, Pot_acionada, Prot, Pnuc, Xs, Ia1, Ea1, Vfase]) # Esse será o motor inicial, que será alterada potencia ou corrente de campo
            flag_grafico_1 += 1
        
        else:

            if msinc_values[-1][1] != Pot_acionada or msinc_values[-1][0]!= If_inicial:
                nova_Pin = Pot_acionada + msinc_values[-1][2] + msinc_values[-1][3]
                Vfase_atual = msinc_values[-1][7]
                Xs_atual = msinc_values[-1][4]
                If_atual = If_inicial
                If_anterior = msinc_values[-1][0]
                Ea_anterior = msinc_values[-1][6]

                # Novo módulo de Ea sempre proporcional ao novo If
                # Se If não mudou, If_atual/If_anterior = 1, então |Ea| permanece igual
                novo_modulo_Ea = abs(Ea_anterior) * (If_atual / If_anterior)

                # Novo ângulo de carga recalculado com base na nova potência e novo |Ea|
                novo_angulo_de_carga = math.asin((nova_Pin * Xs_atual) /
                                                (3 * Vfase_atual * novo_modulo_Ea))

                nova_Ea = cmath.rect(novo_modulo_Ea, -novo_angulo_de_carga)
                novo_angulo_Ea = math.degrees(cmath.phase(nova_Ea))

                nova_Ia = (Vfase_atual - nova_Ea) / (1j * Xs_atual)
                novo_angulo_Ia = math.degrees(cmath.phase(nova_Ia))

                nova_XsIa = 1j * Xs_atual * nova_Ia
                novo_angulo_XsIa = math.degrees(cmath.phase(nova_XsIa))

                delta1_novo = novo_angulo_de_carga  # radianos

                FP_unitario = 1
                magnitud_Ia_fp_unitario = nova_Pin / (3 * Vfase_atual * FP_unitario)
                Ia_fp_unitario = cmath.rect(magnitud_Ia_fp_unitario, -math.acos(FP_unitario))
                Ea_FP_unitario = Vfase_atual - 1j * Xs_atual * Ia_fp_unitario
                If_FP_unitario = (abs(Ea_FP_unitario) * If_atual) / novo_modulo_Ea

                If_max = If_FP_unitario + 1.1
                If_min = If_FP_unitario - 1
                If = np.arange(If_min, If_max, 0.01)

                Ea_2 = (If * novo_modulo_Ea) / If_atual
                # delta2 = np.arcsin(novo_modulo_Ea / abs(Ea_2) * math.sin(delta1_novo))
                ratio = np.clip(novo_modulo_Ea / abs(Ea_2) * math.sin(delta1_novo), -1, 1)
                delta2 = np.arcsin(ratio)
                Ea = Ea_2 * np.exp(1j * -delta2)
                Ia = (Vfase_atual - Ea) / (1j * Xs_atual)

                
                pot_mudou = msinc_values[-1][1] != Pot_acionada  # compara nova_Pin com o estado anterior

                msinc_values.append([If_atual, Pot_acionada, msinc_values[-1][2],
                                    msinc_values[-1][3], Xs_atual,
                                    nova_Ia, nova_Ea, Vfase_atual])

                idx = contador_de_fasores % len(cores_Ea)

                if not pot_mudou:  # potência acionada atual é igual a anterior e só If mudou

                    ax2.plot(If_atual, abs(nova_Ia), marker='o', markersize=8, color=cores_marcador_If[idx],
                            label=f'If = {If_atual} | Ia = {abs(nova_Ia):.2f} A')
                    ax2.legend()
                    
                
                else: # Se a potência mudou plota nova curva V
                    # Curva V
                    ax2.plot(If, abs(Ia), linewidth=2, label=f'Máq. {contador_de_motores} | Pout = {Pot_acionada/746:.1f} HP | If = {If_atual} A')
                    ax2.set_xlabel('Corrente de Campo, A', fontsize=12, fontweight='bold')
                    ax2.set_ylabel('Corrente de Armadura, A', fontsize=12, fontweight='bold')
                    ax2.set_xticks(np.arange(int(min(If)) - 1.5, int(max(If)) + 1.5, 0.25))
                    ax2.set_yticks(range(int(abs(Ia_fp_unitario)) - 1, int(max(abs(Ia))) + 1, 1))
                    ax2.set_title('Corrente de Campo x Corrente de Armadura', fontsize=14, fontweight='bold')
                    ax2.grid(True, alpha=0.3)
                    ax2.plot(If_FP_unitario, abs(Ia_fp_unitario), marker='o', markersize=8, color=cores_marcador_FP1[idx],
                            label=f'FP = 1 | If = {abs(If_FP_unitario):.2f} A | Ia = {abs(Ia_fp_unitario):.2f} A')
                    ax2.plot(If_atual, abs(nova_Ia), marker='o', markersize=8, color=cores_marcador_If[idx],
                            label=f'If = {If_atual} | Ia = {abs(nova_Ia):.2f} A')
                    ax2.legend()


                # Fasores
                fasor = contador_de_fasores * "'"

                ax3.arrow(0, 0, nova_Ea.real, nova_Ea.imag,
                        head_width=7, head_length=8, fc=cores_Ea[idx], ec=cores_Ea[idx],
                        lw=2.5, length_includes_head=True, alpha=0.7,
                        label=f'Ea{fasor} {abs(nova_Ea):.2f} ∠{novo_angulo_Ea:.2f}°')

                ax3.arrow(0, 0, nova_Ia.real, nova_Ia.imag,
                        head_width=5, head_length=6, fc=cores_Ia[idx], ec=cores_Ia[idx],
                        lw=2.5, length_includes_head=True, alpha=0.7,
                        label=f'Ia{fasor} {abs(nova_Ia):.2f} ∠{novo_angulo_Ia:.2f}°')

                ax3.arrow(nova_Ea.real, nova_Ea.imag, nova_XsIa.real, nova_XsIa.imag,
                        head_width=5, head_length=6, fc=cores_XsIa[idx], ec=cores_XsIa[idx],
                        lw=2.5, length_includes_head=True, alpha=0.7,
                        label=f'XsIa{fasor} {abs(nova_XsIa):.2f} ∠{novo_angulo_XsIa:.2f}°')

                valores_limites.extend([abs(nova_Ea.real), abs(nova_Ea.imag),
                                        abs(nova_Ia.real), abs(nova_Ia.imag),
                                        abs(nova_XsIa.real), abs(nova_XsIa.imag)])

                max_val = max(valores_limites)
                ax3.set_xlim(-max_val * 0.3, max_val * 1.3)
                ax3.set_ylim(-max_val, max_val)
                ax3.set_xticks([])
                ax3.set_yticks([])
                ax3.set_xlabel('Real', fontsize=12, fontweight='bold')
                ax3.set_ylabel('Imaginário', fontsize=12, fontweight='bold')
                ax3.set_title('Diagrama Fasorial', fontsize=14, fontweight='bold')
                ax3.grid(True, alpha=0.3)
                ax3.axhline(0, color='black', linewidth=0.8)
                ax3.axvline(0, color='black', linewidth=0.8)
                ax3.legend()

                contador_de_fasores += 1


    qtd_curvas = pop_variation_type.get()

    if qtd_curvas == "Apenas Uma":
        ax2.clear()
        ax3.clear()
        valores_limites.clear()
        msinc_values.clear()
        contador_de_fasores = 0  
        contador_de_motores = 1
        plotar_grafico_unico()
        
    
    elif qtd_curvas == "Duas ou Mais":
        
        if resposta == None or resposta == True:#Se sim, devo congelar todos as outras entrys e permitir somente a atualização da corrente de campo e Potencia acionada
            plotar_multigraficos()
    
        elif resposta == False:
            flag_grafico_1 = 0
            valores_limites.clear()  
            msinc_values.clear()    
            contador_de_motores += 1  
            plotar_multigraficos()
                    

        resposta = messagebox.askyesno(title="Variação de Parâmetros da Máquina", message="Deseja variar os valores da Corrente de Campo e/ou Potência Acionada para essa mesma máquina?")

        inputs_disabled = [input_Vfase, input_polos_msinc, input_f_msinc, status_FP_sgmtd,
                  input_FP_msinc, input_Xs_msinc, input_Prot_msinc, input_Pnuc_msinc]

        if resposta == True:
            for input in inputs_disabled:
                input.configure(state="disabled")
            
            input_Pot_acionada_msinc.configure(border_color="red")
            input_Pot_acionada_msinc.focus()
            input_If_msinc.configure(border_color="red")
            input_If_msinc.focus()

        else:
            for input in inputs_disabled:
                input.configure(state="normal")

            input_Pot_acionada_msinc.configure(border_color="#979DA2")
            input_If_msinc.configure(border_color="#979DA2")
            

    # Atualizar o canvas
    canvas_MSinc.draw()
    canvas_MSinc_vetores.draw()


def clear():
    global ax1
    opcao_selecionada = pop_input_data.get()

    if opcao_selecionada == "Com Dados do MIT":
        # Limpar o gráfico
        ax1.clear()
        canvas_MIT.draw()
    
    else:
        # RESISTÊNCIA DO ESTATOR
        output_R1.configure(state="normal")
        output_R1.delete(0, 'end') # Limpa o valor anterior
        output_R1.configure(state="readonly")

        # REATÂNCIA DO ESTATOR
        output_X1.configure(state="normal")
        output_X1.delete(0, 'end') # Limpa o valor anterior
        output_X1.configure(state="readonly")

        # RESISTÊNCIA DO ROTOR
        output_R2.configure(state="normal")
        output_R2.delete(0, 'end') # Limpa o valor anterior
        output_R2.configure(state="readonly")

        # REATÂNCIA DO ROTOR
        output_X2.configure(state="normal")
        output_X2.delete(0, 'end') # Limpa o valor anterior
        output_X2.configure(state="readonly")

        # REATÂNCIA DE MAGNETIZAÇÃO
        output_Xm.configure(state="normal")
        output_Xm.delete(0, 'end') # Limpa o valor anterior
        output_Xm.configure(state="readonly")


def clear_msinc():
    global flag_grafico_1
    global contador_de_fasores
    global contador_de_motores

     # Limpar o gráfico
    ax2.clear()
    canvas_MSinc.draw()

    # Zera a Flag
    flag_grafico_1 = 0
    contador_de_fasores = 0
    contador_de_motores = 1
    msinc_values.clear() 

    inputs_disabled = [input_Vfase, input_polos_msinc, input_f_msinc, status_FP_sgmtd,
                  input_FP_msinc, input_Xs_msinc, input_Prot_msinc, input_Pnuc_msinc]

    for input in inputs_disabled:
        input.configure(state="normal")

    input_Pot_acionada_msinc.configure(border_color="#979DA2")
    input_If_msinc.configure(border_color="#979DA2")

    ax3.clear()
    ax3.set_xticks([])
    ax3.set_yticks([])
    canvas_MSinc_vetores.draw()



def plot_Tind_x_angulo_de_carga():

    Vfase = 208
    Pnominal = 45*746
    P_acionada = 30*746 #HP -> W
    Xs = 2.5
    f = 60
    polos = 4
    Pnuc = 1000
    Pvent = 1500
    FP = 0.8
    status_FP = "adiantado"
    Pin = P_acionada + Pnuc + Pvent

    
    

    nm=(120*f)/polos # Velocidade síncrona
    omega = ((math.pi)/30)*nm # Velocidade síncrona em rad/s

    Tout = P_acionada/omega

    magnitud_Ia = Pnominal / (3 * Vfase * FP)
    Ia = cmath.rect(magnitud_Ia, math.acos(FP)) ############################################################ Verificar por que que aqui esta sem (-) sinal de menos e na curva V tem

    if status_FP == "atrasado":
        Ia = cmath.rect(magnitud_Ia, -math.acos(FP))
    
    elif status_FP == "adiantado": 
        Ia = cmath.rect(magnitud_Ia, math.acos(FP))

    print(abs(Ia))

    Ea = Vfase - (1j*Xs*Ia)
    angulo_Ea = math.degrees(cmath.phase(Ea))
    angulo_Ea_radianos = math.radians(angulo_Ea)

    print(abs(Ea))
    print(math.degrees(cmath.phase(Ea)))

    δ = np.arange(0, 90, 0.1) #Em Radianos
    δ_radianos = np.radians(δ)

    Tind = (3 * Vfase * abs(Ea) * np.sin(δ_radianos)) / (omega * Xs)

    Tmax = (3 * Vfase * abs(Ea)) / (omega * Xs)

    T_saida = (3 * Vfase * abs(Ea) * np.sin(-angulo_Ea_radianos)) / (omega * Xs)

    print(Tout)
    print(T_saida)
    print(P_acionada)
    # print(Tind)

    # GRÁFICO 2: Tind x δ (Ângulo de Carga)
    ax2.plot(δ, Tind, 'r-', linewidth=2, label='Conjugado Induzido')
    ax2.set_xlabel('δ (Ângulo de Carga) ', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Conjugado Induzido, A', fontsize=12, fontweight='bold')
    # ax2.set_xticks(np.arange(int(min(If))-1.5, int(max(If)) + 1.5, 0.25))
    # ax2.set_yticks(range(int(abs(Ia_fp_unitario))-1, int(max(abs(Ia))) + 1, 1))
    ax2.set_title('Conjugado Induxido x δ (Ângulo de Carga)', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.legend()

    # Marcar pontos importantes no gráfico de corrente
    ax2.plot(max(δ), max(Tind), 'mo', markersize=8, label=f'Conj. Máximo = {max(Tind):.2f} N.m')
    ax2.plot(-angulo_Ea, T_saida, 'go', markersize=8, label=f'Conj. de Operação = {T_saida:.2f} N.m')
    ax2.legend()

    # Atualizar o canvas
    canvas_MSinc.draw()


# Função para transitar de uma seção para outra
def show_Frame(Frame):
    for frame in lista_Frames:
        if frame != Frame:
            frame.place_forget()
    Frame.place(relwidth=0.957, relheight=0.989, relx=0.04, rely=0.004)

#Flags e validações do MIT
Flag_rotor = 0
Flag_graph = 0

#Flags e validações do MSINC
msinc_values = []
valores_limites = []
resposta = None
flag_grafico_1 = 0
contador_de_fasores = 0
contador_de_motores = 1
cores_Ea   = ['blue',   'darkblue',  'royalblue',  'steelblue']
cores_Ia   = ['red',    'darkred',   'crimson',     'salmon']
cores_XsIa = ['purple', 'darkviolet','mediumpurple','plum']
cores_marcador_FP1 = ['green', 'darkgreen', 'limegreen', 'olive']
cores_marcador_If  = ['magenta', 'purple', 'deeppink', 'darkviolet']

app = ctk.CTk()
app.title("M/AC - Simulator")

# Aparência
ctk.set_appearance_mode("light")

app.after(100, lambda: app.state('zoomed'))  # Fullscreen
ctk.deactivate_automatic_dpi_awareness()  # Automatic scaling

lista_Frames = []

#FONTES
font_Title = ctk.CTkFont(family="Arial", size=25, weight="bold")
fonte_subtittle = ctk.CTkFont(family="Arial", size=20, weight="bold")
font_subsub = ctk.CTkFont(family="Cambria Math", size=18, weight="bold")
font_normal = ctk.CTkFont(family="Cambria Math", size=15)
font_msinc = ctk.CTkFont(family="Cambria Math", size=18)
font_input_msinc = ctk.CTkFont(family="Cambria Math", size=18)
font_popup = ctk.CTkFont(family="Arial", size=14)
font_btn = ctk.CTkFont(family="Arial", size=16, weight="bold")

# Frame que ocupa toda a tela
frame_0 = ctk.CTkFrame(app, corner_radius=10)
frame_0.place(relwidth=0.99, relheight=0.982, relx=0.005, rely=0.01)

navigation_bar = ctk.CTkFrame(frame_0, fg_color='#1e0046', bg_color='#dbdbdb',
                                corner_radius=10)
navigation_bar.place(relwidth=0.035, relheight=0.989, relx=0.002, rely=0.004)


frame_Home = ctk.CTkFrame(frame_0, corner_radius=10)
frame_Home.place(relwidth=0.957, relheight=0.989, relx=0.04, rely=0.004)
lista_Frames.append(frame_Home)

# ================================================================================
#                         PÁGINA INICIAL - HOME
# ================================================================================

# Container principal com scroll
scroll_home = ctk.CTkScrollableFrame(
    frame_Home,
    fg_color="transparent",
    scrollbar_button_color="#1e0046",
    scrollbar_button_hover_color="#420f85"
)
scroll_home.pack(fill="both", expand=True, padx=30, pady=30)

# ===== CABEÇALHO =====
frame_header_home = ctk.CTkFrame(scroll_home, fg_color="#1e0046", corner_radius=15)
frame_header_home.pack(fill="x", pady=(0, 25))

# Título principal
titulo_home = ctk.CTkLabel(
    frame_header_home,
    text="⚡ SIMULADOR DE MÁQUINAS ELÉTRICAS CA ⚡",
    font=ctk.CTkFont(family="Arial", size=32, weight="bold"),
    text_color="#ffffff"
)
titulo_home.pack(pady=(25, 10))

# Subtítulo
subtitulo_home = ctk.CTkLabel(
    frame_header_home,
    text="Motores de Indução Trifásicos & Motores Síncronos",
    font=ctk.CTkFont(family="Arial", size=18),
    text_color="#d4d4ff"
)
subtitulo_home.pack(pady=(0, 25))

# ===== SOBRE A APLICAÇÃO =====
frame_sobre = ctk.CTkFrame(scroll_home, fg_color="#2a0055", corner_radius=12)
frame_sobre.pack(fill="x", pady=(0, 20))

titulo_sobre = ctk.CTkLabel(
    frame_sobre,
    text="📋 SOBRE A APLICAÇÃO",
    font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
    text_color="#ffffff",
    anchor="w"
)
titulo_sobre.pack(fill="x", padx=25, pady=(20, 12))

texto_sobre = ctk.CTkLabel(
    frame_sobre,
    text=(
        "Este simulador foi desenvolvido como ferramenta educacional interativa para "
        "o estudo aprofundado de Máquinas de Corrente Alternada. A aplicação permite "
        "visualizar e analisar o comportamento dinâmico de motores elétricos através "
        "de simulações baseadas em equações matemáticas complexas.\n\n"
        "Através de uma interface gráfica intuitiva, é possível simular curvas características "
        "como torque × velocidade, corrente × velocidade, potência, eficiência e outros "
        "parâmetros fundamentais para o entendimento completo do funcionamento dessas máquinas."
    ),
    font=ctk.CTkFont(family="Arial", size=13),
    text_color="#e8e8ff",
    anchor="w",
    justify="left",
    wraplength=1100
)
texto_sobre.pack(fill="x", padx=25, pady=(0, 20))

# ===== OBJETIVO =====
frame_objetivo = ctk.CTkFrame(scroll_home, fg_color="#2a0055", corner_radius=12)
frame_objetivo.pack(fill="x", pady=(0, 20))

titulo_objetivo = ctk.CTkLabel(
    frame_objetivo,
    text="🎯 OBJETIVO",
    font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
    text_color="#ffffff",
    anchor="w"
)
titulo_objetivo.pack(fill="x", padx=25, pady=(20, 12))

texto_objetivo = ctk.CTkLabel(
    frame_objetivo,
    text=(
        "Proporcionar uma alternativa didática e visual para complementar o aprendizado "
        "teórico de estudantes de Engenharia Elétrica e áreas correlatas. A ferramenta "
        "permite:\n\n"
        "• Validação prática dos conceitos teóricos estudados\n"
        "• Análise comparativa entre diferentes configurações de motores\n"
        "• Compreensão intuitiva dos fenômenos eletromagnéticos\n"
        "• Experimentação segura com parâmetros variados\n"
        "• Visualização gráfica de características operacionais"
    ),
    font=ctk.CTkFont(family="Arial", size=13),
    text_color="#e8e8ff",
    anchor="w",
    justify="left",
    wraplength=1100
)
texto_objetivo.pack(fill="x", padx=25, pady=(0, 20))

# ===== FUNCIONALIDADES =====
frame_funcionalidades = ctk.CTkFrame(scroll_home, fg_color="#2a0055", corner_radius=12)
frame_funcionalidades.pack(fill="x", pady=(0, 20))

titulo_funcionalidades = ctk.CTkLabel(
    frame_funcionalidades,
    text="⚙️ FUNCIONALIDADES",
    font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
    text_color="#ffffff",
    anchor="w"
)
titulo_funcionalidades.pack(fill="x", padx=25, pady=(20, 12))

texto_funcionalidades = ctk.CTkLabel(
    frame_funcionalidades,
    text=(
        "✓ Simulação de Motores de Indução Trifásicos (MIT)\n"
        "✓ Simulação de Motores Síncronos\n"
        "✓ Geração de curvas características\n"
        "✓ Ajuste de parâmetros elétricos e mecânicos\n"
        "✓ Duas modalidades para máquinas de indução: Com Dados do MIT e Com Dados de Ensaio\n"
        "✓ Visualização gráfica profissional com Matplotlib\n"
        "✓ Cálculo automático de parâmetros do circuito equivalente\n"
        "✓ Interface intuitiva e responsiva"
    ),
    font=ctk.CTkFont(family="Arial", size=13),
    text_color="#e8e8ff",
    anchor="w",
    justify="left",
    wraplength=1100
)
texto_funcionalidades.pack(fill="x", padx=25, pady=(0, 20))

# ===== DESENVOLVIMENTO (TCC) =====
frame_desenvolvimento = ctk.CTkFrame(scroll_home, fg_color="#2a0055", corner_radius=12)
frame_desenvolvimento.pack(fill="x", pady=(0, 20))

titulo_desenvolvimento = ctk.CTkLabel(
    frame_desenvolvimento,
    text="👨‍🎓 DESENVOLVIMENTO",
    font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
    text_color="#ffffff",
    anchor="w"
)
titulo_desenvolvimento.pack(fill="x", padx=25, pady=(20, 12))

texto_desenvolvimento = ctk.CTkLabel(
    frame_desenvolvimento,
    text=(
        "Esta aplicação foi desenvolvida como Trabalho de Conclusão de Curso (TCC), "
        "integrando conhecimentos de:\n\n"
        "• Máquinas Elétricas e Acionamentos\n"
        "• Modelagem Matemática\n"
        "• Programação Científica em Python\n"
        "• Interface Humano-Computador (IHC)\n\n"
        "O desenvolvimento contemplou extenso estudo teórico, implementação computacional "
        "e validação dos resultados com dados de referência da literatura técnica especializada."
    ),
    font=ctk.CTkFont(family="Arial", size=13),
    text_color="#e8e8ff",
    anchor="w",
    justify="left",
    wraplength=1100
)
texto_desenvolvimento.pack(fill="x", padx=25, pady=(0, 20))

# ===== TECNOLOGIAS =====
frame_tecnologias = ctk.CTkFrame(scroll_home, fg_color="#1e0046", corner_radius=12)
frame_tecnologias.pack(fill="x", pady=(0, 25))

titulo_tecnologias = ctk.CTkLabel(
    frame_tecnologias,
    text="💻 TECNOLOGIAS UTILIZADAS",
    font=ctk.CTkFont(family="Arial", size=16, weight="bold"),
    text_color="#ffffff"
)
titulo_tecnologias.pack(pady=(18, 10))

texto_tecnologias = ctk.CTkLabel(
    frame_tecnologias,
    text="Python 3.12.0  •  CustomTkinter  •  Matplotlib  •  NumPy  •  PIL (Pillow)",
    font=ctk.CTkFont(family="Arial", size=14),
    text_color="#d4d4ff"
)
texto_tecnologias.pack(pady=(0, 18))

# ===== INSTRUÇÕES =====
frame_instrucoes = ctk.CTkFrame(scroll_home, fg_color="#2a0055", corner_radius=12)
frame_instrucoes.pack(fill="x", pady=(0, 30))

titulo_instrucoes = ctk.CTkLabel(
    frame_instrucoes,
    text="📖 COMO UTILIZAR",
    font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
    text_color="#ffffff",
    anchor="w"
)
titulo_instrucoes.pack(fill="x", padx=25, pady=(20, 12))

texto_instrucoes = ctk.CTkLabel(
    frame_instrucoes,
    text=(
        "1. Navegue pelo menu lateral para selecionar o tipo de motor a simular:\n"
        "   • Motor de Indução Trifásico (MIT)\n"
        "   • Motor Síncrono (MSINC)\n\n"
        "2. Para o MIT, escolha entre:\n"
        "   • Com Dados do MIT: insira os parâmetros do circuito equivalente\n"
        "   • Com Dados de Ensaio: utilize dados de ensaios laboratoriais\n\n"
        "3. Preencha os campos de entrada com os valores desejados\n\n"
        "4. Selecione o tipo de curva a ser visualizada\n\n"
        "5. Clique em 'SIMULAR' para gerar os gráficos\n\n"
        "Os resultados serão exibidos instantaneamente, permitindo análise detalhada do comportamento da máquina."
    ),
    font=ctk.CTkFont(family="Arial", size=13),
    text_color="#e8e8ff",
    anchor="w",
    justify="left",
    wraplength=1100
)
texto_instrucoes.pack(fill="x", padx=25, pady=(0, 20))

# ===== RODAPÉ =====
frame_footer_home = ctk.CTkFrame(scroll_home, fg_color="transparent")
frame_footer_home.pack(fill="x", pady=(10, 0))

nota_rodape = ctk.CTkLabel(
    frame_footer_home,
    text="Desenvolvido como contribuição acadêmica para o ensino de Engenharia Elétrica\nUtilize o menu lateral para acessar as ferramentas de simulação",
    font=ctk.CTkFont(family="Arial", size=12, slant="italic"),
    text_color="#9090c0",
    justify="center"
)
nota_rodape.pack(pady=(15, 10))

# ================================================================================
#                         FIM DA PÁGINA INICIAL
# ================================================================================


frame_MIT = ctk.CTkFrame(frame_0, corner_radius=10)
frame_MIT.place(relwidth=0.957, relheight=0.989, relx=0.04, rely=0.004)
lista_Frames.append(frame_MIT)

frame_MSinc = ctk.CTkFrame(frame_0, corner_radius=10)
frame_MSinc.place(relwidth=0.957, relheight=0.989, relx=0.04, rely=0.004)
lista_Frames.append(frame_MSinc)


Home_path = resource_path("Home_bracno28x22.png")
imagem_home = ctk.CTkImage(light_image=Image.open(Home_path), size=(28, 22))
btn_Home = ctk.CTkButton(navigation_bar, text="", fg_color='#1e0046', hover_color="#420f85",
                        image=imagem_home, command=lambda: show_Frame(frame_Home))
btn_Home.place(relwidth=1, relheight=0.09, rely=0.05)

btn_MIT = ctk.CTkButton(navigation_bar, text="MIT", fg_color='#1e0046', hover_color="#420f85",
                        font=font_btn, command=lambda: show_Frame(frame_MIT))
btn_MIT.place(relwidth=1, relheight=0.09, rely=0.14)

btn_MSinc = ctk.CTkButton(navigation_bar, text="MSINC", fg_color='#1e0046', hover_color="#420f85",
                          font=font_btn, command=lambda: show_Frame(frame_MSinc))
btn_MSinc.place(relwidth=1, relheight=0.09, rely=0.231)



fig_MIT = Figure(figsize=(10,9), facecolor="#CFCFCF")
# ax1 = fig_MIT.add_subplot(1, 1, 1)

canvas_MIT = FigureCanvasTkAgg(fig_MIT, master=frame_MIT) #   Gráfico MIT
# canvas_MIT.draw()
canvas_MIT.get_tk_widget().place(x=890, y=-40)


circuito_path = resource_path("circuito_eq_MIT.jpg")
imagem_circuito = ctk.CTkImage(light_image=Image.open(circuito_path), size=(800, 700))
# Criar um Label para exibir a imagem (sem texto)
label_circuito_MIT = ctk.CTkLabel(frame_MIT, image=imagem_circuito, text="")
# Posicionar a imagem no frame usando place


fig_MSinc = Figure(figsize=(10,9), facecolor="#CFCFCF")
ax2 = fig_MSinc.add_subplot(1, 1, 1)

canvas_MSinc = FigureCanvasTkAgg(fig_MSinc, master=frame_MSinc) #   Gráfico MSINC
canvas_MSinc.draw()
canvas_MSinc.get_tk_widget().place(x=-45, y=-70)


fig_MSinc_vetores = Figure(figsize=(10,9), facecolor="#CFCFCF")
ax3 = fig_MSinc_vetores.add_subplot(1, 1, 1)
# ✅ Remover os números dos eixos
ax3.set_xticks([])
ax3.set_yticks([])

canvas_MSinc_vetores = FigureCanvasTkAgg(fig_MSinc_vetores, master=frame_MSinc) #   Gráfico MSINC vetores
canvas_MSinc_vetores.draw()
canvas_MSinc_vetores.get_tk_widget().place(x=860, y=-70)



txt_input_data = ctk.CTkLabel(frame_MIT, text="DADOS DE ENTRADA", font=fonte_subtittle, )
txt_input_data.place(relwidth=0.12, relheight=0.04, relx=0.01, rely=0.03)
pop_input_data = ctk.CTkOptionMenu(frame_MIT, values=["Com Dados do MIT", "Com Dados de Ensaio"],
                                   fg_color="#ffffff", button_color="#1e0046", text_color="#656565",
                                   font=font_popup, command=opcao_selecionada, button_hover_color="#420f85")
pop_input_data.place(relwidth=0.1, relheight=0.03, relx=0.02, rely=0.08)
pop_input_data.set(" ")

txt_rotor_type = ctk.CTkLabel(frame_MIT, text="TIPO DO ROTOR", font=fonte_subtittle)
txt_rotor_type.place(relwidth=0.12, relheight=0.04, relx=0.133, rely=0.03)
pop_rotor_type = ctk.CTkOptionMenu(frame_MIT, values=["Gaiola de Esquilo", "Bobinado"],
                                   fg_color="#ffffff", button_color="#1e0046", text_color="#656565",
                                   font=font_popup, state="disabled", button_hover_color="#420f85")
pop_rotor_type.place(relwidth=0.1, relheight=0.03, relx=0.145, rely=0.08)


txt_Graphs = ctk.CTkLabel(frame_MIT, text="GRÁFICOS", font=fonte_subtittle)
txt_Graphs.place(relwidth=0.12, relheight=0.04, relx=0.263, rely=0.03)
pop_graphs = ctk.CTkOptionMenu(frame_MIT, values=["Conjugado X Velocidade", "Corrente X Velocidade"],
                                   fg_color="#ffffff", button_color="#1e0046", text_color="#656565",
                                   font=font_popup, state="disabled", button_hover_color="#420f85")
pop_graphs.place(relwidth=0.11, relheight=0.03, relx=0.27, rely=0.08)


txt_category = ctk.CTkLabel(frame_MIT, text="CATEGORIA", font=fonte_subtittle)
txt_category.place(relwidth=0.12, relheight=0.04, relx=0.4, rely=0.03)
pop_category = ctk.CTkOptionMenu(frame_MIT, values=["Categoria N", "Categoria H", "Categoria D"],
                                   fg_color="#ffffff", button_color="#1e0046", text_color="#656565",
                                   font=font_popup, state="disabled", button_hover_color="#420f85")
pop_category.place(relwidth=0.11, relheight=0.03, relx=0.41, rely=0.08)


# ================================================================================

#                               MOTOR DE INDUÇÃO

# ================================================================================

##======================    DADOS DE ENTRADA DO MIT    ==========================


txt_MIT_data = ctk.CTkLabel(frame_MIT, text="DADOS DO MIT", font=font_Title)
txt_MIT_data.place(relwidth=0.11, relheight=0.04, relx=0.03, rely=0.13)

input_polos = ctk.CTkEntry(frame_MIT, justify='center', state="disabled")
input_polos.place(relwidth=0.03, relheight=0.04, relx=0.13, rely=0.19)
txt_polos = ctk.CTkLabel(frame_MIT, text="Número de Polos", anchor="w", font=font_normal)
txt_polos.place(relwidth=0.1, relheight=0.04, relx=0.01, rely=0.19)

input_Vlinha = ctk.CTkEntry(frame_MIT, justify='center', state="disabled")
input_Vlinha.place(relwidth=0.03, relheight=0.04, relx=0.13, rely=0.26)
txt_Vlinha = ctk.CTkLabel(frame_MIT, text="Tensão de Linha (V)", anchor="w", font=font_normal)
txt_Vlinha.place(relwidth=0.1, relheight=0.04, relx=0.01, rely=0.26)

input_f = ctk.CTkEntry(frame_MIT, justify='center', state="disabled")
input_f.place(relwidth=0.03, relheight=0.04, relx=0.13, rely=0.33)
txt_f = ctk.CTkLabel(frame_MIT, text="Frequência do Estator (Hz)", anchor="w", font=font_normal)
txt_f.place(relwidth=0.1, relheight=0.04, relx=0.01, rely=0.33)

input_R1 = ctk.CTkEntry(frame_MIT, justify='center', state="disabled")
input_R1.place(relwidth=0.03, relheight=0.04, relx=0.13, rely=0.4)
txt_R1 = ctk.CTkLabel(frame_MIT, text="Resistência do Estator (Ω)", anchor="w", font=font_normal)
txt_R1.place(relwidth=0.1, relheight=0.04, relx=0.01, rely=0.4)

input_R2 = ctk.CTkEntry(frame_MIT, justify='center', state="disabled")
input_R2.place(relwidth=0.03, relheight=0.04, relx=0.13, rely=0.47)
txt_R2 = ctk.CTkLabel(frame_MIT, text="Resistência do Rotor (Ω)", anchor="w", font=font_normal)
txt_R2.place(relwidth=0.1, relheight=0.04, relx=0.01, rely=0.47)

input_X1 = ctk.CTkEntry(frame_MIT, justify='center', state="disabled")
input_X1.place(relwidth=0.03, relheight=0.04, relx=0.13, rely=0.54)
txt_X1 = ctk.CTkLabel(frame_MIT, text="Reatância do Estator (Ω)", anchor="w", font=font_normal)
txt_X1.place(relwidth=0.1, relheight=0.04, relx=0.01, rely=0.54)

input_X2 = ctk.CTkEntry(frame_MIT, justify='center', state="disabled")
input_X2.place(relwidth=0.03, relheight=0.04, relx=0.13, rely=0.61)
txt_X2 = ctk.CTkLabel(frame_MIT, text="Reatância do Rotor (Ω)", anchor="w", font=font_normal)
txt_X2.place(relwidth=0.1, relheight=0.04, relx=0.01, rely=0.61)

input_Xm = ctk.CTkEntry(frame_MIT, justify='center', state="disabled")
input_Xm.place(relwidth=0.03, relheight=0.04, relx=0.13, rely=0.68)
txt_Xm = ctk.CTkLabel(frame_MIT, text="Reatância de Magnetização (Ω)", anchor="w", font=font_normal)
txt_Xm.place(relwidth=0.11, relheight=0.04, relx=0.01, rely=0.68)

input_s = ctk.CTkEntry(frame_MIT, justify='center', state="disabled")
input_s.place(relwidth=0.03, relheight=0.04, relx=0.13, rely=0.75)
txt_s = ctk.CTkLabel(frame_MIT, text="Escorregamento Nominal (%)", anchor="w", font=font_normal)
txt_s.place(relwidth=0.11, relheight=0.04, relx=0.01, rely=0.75)

input_Pvent = ctk.CTkEntry(frame_MIT, justify='center', state="disabled")
input_Pvent.place(relwidth=0.03, relheight=0.04, relx=0.13, rely=0.82)
txt_Pvent = ctk.CTkLabel(frame_MIT, text="Perdas p/ Atrito e Ventilação (W)", anchor="w", font=font_normal)
txt_Pvent.place(relwidth=0.12, relheight=0.04, relx=0.01, rely=0.82)

input_Pnuc = ctk.CTkEntry(frame_MIT, justify='center', state="disabled")
input_Pnuc.place(relwidth=0.03, relheight=0.04, relx=0.13, rely=0.89)
txt_Pnuc = ctk.CTkLabel(frame_MIT, text="Perdas no Núcleo (W)", anchor="w", font=font_normal)
txt_Pnuc.place(relwidth=0.1, relheight=0.04, relx=0.01, rely=0.89)

btn_simular_curva = ctk.CTkButton(frame_MIT, text="SIMULAR", font=font_Title, fg_color='#1e0046', hover_color="#420f85",
                                  command=plot_Graphical)


btn_calcular_circuito = ctk.CTkButton(frame_MIT, text="CALCULAR", font=font_Title, fg_color='#1e0046', hover_color="#420f85",
                                  command=calculate_circuit)

btn_clear = ctk.CTkButton(frame_MIT, text="LIMPAR", font=font_Title, fg_color="#A50404", hover_color="#E30D0D",
                          command=clear)



##======================    DADOS DE SAÍDA DO MIT    ==========================


txt_Resultados = ctk.CTkLabel(frame_MIT, text="RESULTADOS", font=font_Title)
txt_Resultados.place(relwidth=0.1, relheight=0.04, relx=0.31, rely=0.48)

txt_Tmax = ctk.CTkLabel(frame_MIT, text="Conjugado Máximo", anchor="w", font=font_normal)
txt_Tmax.place(relwidth=0.1, relheight=0.04, relx=0.18, rely=0.54)
output_Tmax = ctk.CTkEntry(frame_MIT, justify='center', state="readonly")
output_Tmax.place(relwidth=0.032, relheight=0.04, relx=0.285, rely=0.54)
txt_Tmax_unit = ctk.CTkLabel(frame_MIT, text="(N.m)", font=font_normal)
txt_Tmax_unit.place(relwidth=0.02, relheight=0.04, relx=0.32, rely=0.54)

txt_Vel_Tmax = ctk.CTkLabel(frame_MIT, text="Velocidade (Conj. Máximo)", anchor="w", font=font_normal)
txt_Vel_Tmax.place(relwidth=0.1, relheight=0.04, relx=0.18, rely=0.6)
output_Vel_Tmax = ctk.CTkEntry(frame_MIT, justify='center', state="readonly")
output_Vel_Tmax.place(relwidth=0.032, relheight=0.04, relx=0.285, rely=0.6)
txt__Vel_Tmax = ctk.CTkLabel(frame_MIT, text="(rpm)", font=font_normal)
txt__Vel_Tmax.place(relwidth=0.02, relheight=0.04, relx=0.32, rely=0.6)

txt_Tpart = ctk.CTkLabel(frame_MIT, text="Conjugado de Partida", anchor="w", font=font_normal)
txt_Tpart.place(relwidth=0.1, relheight=0.04, relx=0.18, rely=0.66)
output_Tpart = ctk.CTkEntry(frame_MIT, justify='center', state="readonly")
output_Tpart.place(relwidth=0.032, relheight=0.04, relx=0.285, rely=0.66)
txt__Tpart = ctk.CTkLabel(frame_MIT, text="(N.m)", font=font_normal)
txt__Tpart.place(relwidth=0.02, relheight=0.04, relx=0.32, rely=0.66)

txt_Vel_Nom = ctk.CTkLabel(frame_MIT, text="Velocidade Nominal", anchor="w", font=font_normal)
txt_Vel_Nom.place(relwidth=0.1, relheight=0.04, relx=0.18, rely=0.72)
output_Vel_Nom = ctk.CTkEntry(frame_MIT, justify='center', state="readonly")
output_Vel_Nom.place(relwidth=0.032, relheight=0.04, relx=0.285, rely=0.72)
txt__Vel_Nom = ctk.CTkLabel(frame_MIT, text="(rpm)", font=font_normal)
txt__Vel_Nom.place(relwidth=0.02, relheight=0.04, relx=0.32, rely=0.72)

txt_Efic = ctk.CTkLabel(frame_MIT, text="Eficiência", anchor="w", font=font_normal)
txt_Efic.place(relwidth=0.1, relheight=0.04, relx=0.18, rely=0.78)
output_Efic = ctk.CTkEntry(frame_MIT, justify='center', state="readonly")
output_Efic.place(relwidth=0.032, relheight=0.04, relx=0.285, rely=0.78)
txt__Efic = ctk.CTkLabel(frame_MIT, text="(%)", font=font_normal)
txt__Efic.place(relwidth=0.02, relheight=0.04, relx=0.32, rely=0.78)

txt_I_Part = ctk.CTkLabel(frame_MIT, text="Corrente de Partida", anchor="w", font=font_normal)
txt_I_Part.place(relwidth=0.1, relheight=0.04, relx=0.18, rely=0.84)
output_I_Part = ctk.CTkEntry(frame_MIT, justify='center', state="readonly")
output_I_Part.place(relwidth=0.032, relheight=0.04, relx=0.285, rely=0.84)
txt__I_Part = ctk.CTkLabel(frame_MIT, text="(A)", font=font_normal)
txt__I_Part.place(relwidth=0.02, relheight=0.04, relx=0.32, rely=0.84)

txt_I_Nom = ctk.CTkLabel(frame_MIT, text="Corrente Nominal", anchor="w", font=font_normal)
txt_I_Nom.place(relwidth=0.1, relheight=0.04, relx=0.18, rely=0.9)
output_I_Nom = ctk.CTkEntry(frame_MIT, justify='center', state="readonly")
output_I_Nom.place(relwidth=0.032, relheight=0.04, relx=0.285, rely=0.9)
txt__I_Nom = ctk.CTkLabel(frame_MIT, text="(A)", font=font_normal)
txt__I_Nom.place(relwidth=0.02, relheight=0.04, relx=0.32, rely=0.9)

txt_Pin = ctk.CTkLabel(frame_MIT, text="Potência de Entrada", anchor="w", font=font_normal)
txt_Pin.place(relwidth=0.1, relheight=0.04, relx=0.36, rely=0.54)
output_Pin = ctk.CTkEntry(frame_MIT, justify='center', state="readonly")
output_Pin.place(relwidth=0.032, relheight=0.04, relx=0.465, rely=0.54)
txt_Pin = ctk.CTkLabel(frame_MIT, text="(W)", font=font_normal)
txt_Pin.place(relwidth=0.02, relheight=0.04, relx=0.5, rely=0.54)

txt_PCE = ctk.CTkLabel(frame_MIT, text="Perdas no Cobre do Estator", anchor="w", font=font_normal)
txt_PCE.place(relwidth=0.1, relheight=0.04, relx=0.36, rely=0.6)
output_PCE = ctk.CTkEntry(frame_MIT, justify='center', state="readonly")
output_PCE.place(relwidth=0.032, relheight=0.04, relx=0.465, rely=0.6)
txt_PCE = ctk.CTkLabel(frame_MIT, text="(W)", font=font_normal)
txt_PCE.place(relwidth=0.02, relheight=0.04, relx=0.5, rely=0.6)

txt_PEF = ctk.CTkLabel(frame_MIT, text="Potência de Entreferro", anchor="w", font=font_normal)
txt_PEF.place(relwidth=0.1, relheight=0.04, relx=0.36, rely=0.66)
output_PEF = ctk.CTkEntry(frame_MIT, justify='center', state="readonly")
output_PEF.place(relwidth=0.032, relheight=0.04, relx=0.465, rely=0.66)
txt_PEF = ctk.CTkLabel(frame_MIT, text="(W)", font=font_normal)
txt_PEF.place(relwidth=0.02, relheight=0.04, relx=0.5, rely=0.66)

txt_Pconv = ctk.CTkLabel(frame_MIT, text="Potência Convertida", anchor="w", font=font_normal)
txt_Pconv.place(relwidth=0.1, relheight=0.04, relx=0.36, rely=0.72)
output_Pconv = ctk.CTkEntry(frame_MIT, justify='center', state="readonly")
output_Pconv.place(relwidth=0.032, relheight=0.04, relx=0.465, rely=0.72)
txt_Pconv = ctk.CTkLabel(frame_MIT, text="(W)", font=font_normal)
txt_Pconv.place(relwidth=0.02, relheight=0.04, relx=0.5, rely=0.72)

txt_Pout = ctk.CTkLabel(frame_MIT, text="Potência de Saída", anchor="w", font=font_normal)
txt_Pout.place(relwidth=0.1, relheight=0.04, relx=0.36, rely=0.78)
output_Pout = ctk.CTkEntry(frame_MIT, justify='center', state="readonly")
output_Pout.place(relwidth=0.032, relheight=0.04, relx=0.465, rely=0.78)
txt_Pout = ctk.CTkLabel(frame_MIT, text="(W)", font=font_normal)
txt_Pout.place(relwidth=0.02, relheight=0.04, relx=0.5, rely=0.78)

txt_Tind = ctk.CTkLabel(frame_MIT, text="Conjugado Induzido", anchor="w", font=font_normal)
txt_Tind.place(relwidth=0.1, relheight=0.04, relx=0.36, rely=0.84)
output_Tind = ctk.CTkEntry(frame_MIT, justify='center', state="readonly")
output_Tind.place(relwidth=0.032, relheight=0.04, relx=0.465, rely=0.84)
txt_Tind = ctk.CTkLabel(frame_MIT, text="(N.m)", font=font_normal)
txt_Tind.place(relwidth=0.02, relheight=0.04, relx=0.5, rely=0.84)

txt_Tout = ctk.CTkLabel(frame_MIT, text="Conjugado de Saída", anchor="w", font=font_normal)
txt_Tout.place(relwidth=0.1, relheight=0.04, relx=0.36, rely=0.9)
output_Tout = ctk.CTkEntry(frame_MIT, justify='center', state="readonly")
output_Tout.place(relwidth=0.032, relheight=0.04, relx=0.465, rely=0.9)
txt_Tout = ctk.CTkLabel(frame_MIT, text="(N.m)", font=font_normal)
txt_Tout.place(relwidth=0.02, relheight=0.04, relx=0.5, rely=0.9)


##======================    DADOS DE ENSAIO    ==========================

txt_dados_de_ensaio = ctk.CTkLabel(frame_MIT, text="DADOS DE ENSAIO", font=font_Title)
txt_dados_de_ensaio.place(relwidth=0.13, relheight=0.04, relx=0.295, rely=0.13)

# ------------------------ DADOS DE ENTRADA -------------------------

#---------- ENSAIO CC ---------
input_Vcc = ctk.CTkEntry(frame_MIT, justify='center', state="disabled")
input_Vcc.place(relwidth=0.03, relheight=0.04, relx=0.3, rely=0.22)
txt_Vcc = ctk.CTkLabel(frame_MIT, text="Vcc", font=font_normal)
txt_Vcc.place(relwidth=0.05, relheight=0.04, relx=0.29, rely=0.18)

input_Icc = ctk.CTkEntry(frame_MIT, justify='center', state="disabled")
input_Icc.place(relwidth=0.03, relheight=0.04, relx=0.385, rely=0.22)
txt_Icc = ctk.CTkLabel(frame_MIT, text="Icc", font=font_normal)
txt_Icc.place(relwidth=0.05, relheight=0.04, relx=0.375, rely=0.18)

txt_Ensaio_vz = ctk.CTkLabel(frame_MIT, text="Ensaio CC", font=font_subsub)
txt_Ensaio_vz.place(relwidth=0.06, relheight=0.03, relx=0.325, rely=0.16)

#---------- ENSAIO A VAZIO ---------
txt_Ensaio_vz = ctk.CTkLabel(frame_MIT, text="Ensaio a Vazio", font=font_subsub)
txt_Ensaio_vz.place(relwidth=0.07, relheight=0.03, relx=0.24, rely=0.27)

input_Vt_vz = ctk.CTkEntry(frame_MIT, justify='center', state="disabled")
input_Vt_vz.place(relwidth=0.03, relheight=0.04, relx=0.22, rely=0.34)
txt_Vt_vz = ctk.CTkLabel(frame_MIT, text="Vt", font=font_normal)
txt_Vt_vz.place(relwidth=0.05, relheight=0.04, relx=0.21, rely=0.3)

input_Il_vz = ctk.CTkEntry(frame_MIT, justify='center', state="disabled")
input_Il_vz.place(relwidth=0.03, relheight=0.04, relx=0.3, rely=0.34)
txt_Il_vz = ctk.CTkLabel(frame_MIT, text="Il", font=font_normal)
txt_Il_vz.place(relwidth=0.05, relheight=0.04, relx=0.29, rely=0.3)

input_frequency_vz = ctk.CTkEntry(frame_MIT, justify='center', state="disabled")
input_frequency_vz.place(relwidth=0.03, relheight=0.04, relx=0.22, rely=0.42)
txt_frequency_vz = ctk.CTkLabel(frame_MIT, text="Frequência", font=font_normal)
txt_frequency_vz.place(relwidth=0.05, relheight=0.04, relx=0.21, rely=0.38)

input_Pin_vz = ctk.CTkEntry(frame_MIT, justify='center', state="disabled")
input_Pin_vz.place(relwidth=0.03, relheight=0.04, relx=0.3, rely=0.42)
txt_Pin_vz = ctk.CTkLabel(frame_MIT, text="Pin", font=font_normal)
txt_Pin_vz.place(relwidth=0.05, relheight=0.04, relx=0.29, rely=0.38)


#---------- ENSAIO DE ROTOR BLOQUEADO ---------
txt_Ensaio_rb = ctk.CTkLabel(frame_MIT, text="Ensaio de Rotor Bloqueado", font=font_subsub)
txt_Ensaio_rb.place(relwidth=0.14, relheight=0.03, relx=0.37, rely=0.27)

input_Vt_rb = ctk.CTkEntry(frame_MIT, justify='center', state="disabled")
input_Vt_rb.place(relwidth=0.03, relheight=0.04, relx=0.385, rely=0.34)
txt_Vt_rb = ctk.CTkLabel(frame_MIT, text="Vt", font=font_normal)
txt_Vt_rb.place(relwidth=0.05, relheight=0.04, relx=0.375, rely=0.3)

input_Il_rb = ctk.CTkEntry(frame_MIT, justify='center', state="disabled")
input_Il_rb.place(relwidth=0.03, relheight=0.04, relx=0.465, rely=0.34)
txt_Il_rb = ctk.CTkLabel(frame_MIT, text="Il", font=font_normal)
txt_Il_rb.place(relwidth=0.05, relheight=0.04, relx=0.455, rely=0.3)

input_frequency_rb = ctk.CTkEntry(frame_MIT, justify='center', state="disabled")
input_frequency_rb.place(relwidth=0.03, relheight=0.04, relx=0.385, rely=0.42)
txt_frequency_rb = ctk.CTkLabel(frame_MIT, text="Frequência", font=font_normal)
txt_frequency_rb.place(relwidth=0.05, relheight=0.04, relx=0.375, rely=0.38)

input_Pin_rb = ctk.CTkEntry(frame_MIT, justify='center', state="disabled")
input_Pin_rb.place(relwidth=0.03, relheight=0.04, relx=0.465, rely=0.42)
txt_Pin_rb = ctk.CTkLabel(frame_MIT, text="Pin", font=font_normal)
txt_Pin_rb.place(relwidth=0.05, relheight=0.04, relx=0.455, rely=0.38)


# ------------------------ DADOS DE SAÍDA -------------------------

txt_output_R1 = ctk.CTkLabel(frame_MIT, text="R1", font=font_subsub, fg_color='white', bg_color='white')
output_R1 = ctk.CTkEntry(frame_MIT, justify='center', state="readonly", bg_color='white')

txt_output_X1 = ctk.CTkLabel(frame_MIT, text="X1", font=font_subsub, fg_color='white', bg_color='white')
output_X1 = ctk.CTkEntry(frame_MIT, justify='center', state="readonly", bg_color='white')

txt_output_R2 = ctk.CTkLabel(frame_MIT, text="R2", font=font_subsub, fg_color='white', bg_color='white')
output_R2 = ctk.CTkEntry(frame_MIT, justify='center', state="readonly", bg_color='white')

txt_output_X2 = ctk.CTkLabel(frame_MIT, text="X2", font=font_subsub, fg_color='white', bg_color='white')
output_X2 = ctk.CTkEntry(frame_MIT, justify='center', state="readonly", bg_color='white')

txt_output_Xm = ctk.CTkLabel(frame_MIT, text="Xm", font=font_subsub, fg_color='white', bg_color='white')
output_Xm = ctk.CTkEntry(frame_MIT, justify='center', state="readonly", bg_color='white')



# ================================================================================

#                               MOTOR SÍNCRONO

# ================================================================================


btn_simular_curva_V_msinc = ctk.CTkButton(frame_MSinc, text="SIMULAR", font=font_Title, fg_color='#1e0046', hover_color="#420f85",
                                  command=plot_V_curve)
btn_simular_curva_V_msinc.place(relwidth=0.26, relheight=0.1, relx=0.6, rely=0.87)

# .place(relwidth=0.3, relheight=0.1, relx=0.56, rely=0.87)

btn_clear_msinc = ctk.CTkButton(frame_MSinc, text="LIMPAR", font=font_Title, fg_color="#A50404", hover_color="#E30D0D",
                          command=clear_msinc)
btn_clear_msinc.place(relwidth=0.1, relheight=0.1, relx=0.87, rely=0.87)

# btn_simular_curva_Tind_msinc = ctk.CTkButton(frame_MSinc, text="SIMULAR", font=font_Title, fg_color='#1e0046', hover_color="#420f85",
#                                   command=plot_Tind_x_angulo_de_carga)
# btn_simular_curva_Tind_msinc.place(relwidth=0.3, relheight=0.1, relx=0.56, rely=0.87)

txt_pop_variation_type = ctk.CTkLabel(frame_MSinc, text="QTD. DE CURVAS", font=fonte_subtittle)
txt_pop_variation_type.place(relwidth=0.12, relheight=0.04, relx=0.59, rely=0.78)
pop_variation_type = ctk.CTkOptionMenu(frame_MSinc, values=["Apenas Uma", "Duas ou Mais"],
                                   fg_color="#ffffff", button_color="#1e0046", text_color="#656565",
                                   font=font_popup, state="normal", button_hover_color="#420f85")
pop_variation_type.place(relwidth=0.1, relheight=0.03, relx=0.6, rely=0.82)


txt_Vfase = ctk.CTkLabel(frame_MSinc, text="Tensão de Fase", anchor="w", font=font_msinc)
txt_Vfase.place(relwidth=0.1, relheight=0.04, relx=0.01, rely=0.82)
input_Vfase = ctk.CTkEntry(frame_MSinc, justify='center', font=font_input_msinc)
input_Vfase.place(relwidth=0.03, relheight=0.04, relx=0.1, rely=0.82)
txt_Vfase_unit = ctk.CTkLabel(frame_MSinc, text="(V)", font=font_msinc)
txt_Vfase_unit.place(relwidth=0.02, relheight=0.04, relx=0.135, rely=0.82)


txt_polos_msinc = ctk.CTkLabel(frame_MSinc, text="Polos", anchor="w", font=font_msinc)
txt_polos_msinc.place(relwidth=0.1, relheight=0.04, relx=0.01, rely=0.88)
input_polos_msinc = ctk.CTkEntry(frame_MSinc, justify='center', font=font_input_msinc)
input_polos_msinc.place(relwidth=0.03, relheight=0.04, relx=0.1, rely=0.88)


txt_f_msinc = ctk.CTkLabel(frame_MSinc, text="Frequência", anchor="w", font=font_msinc)
txt_f_msinc.place(relwidth=0.1, relheight=0.04, relx=0.01, rely=0.94)
input_f_msinc = ctk.CTkEntry(frame_MSinc, justify='center', font=font_input_msinc)
input_f_msinc.place(relwidth=0.03, relheight=0.04, relx=0.1, rely=0.94)
txt_f_msinc_unit = ctk.CTkLabel(frame_MSinc, text="(Hz)", font=font_msinc)
txt_f_msinc_unit.place(relwidth=0.02, relheight=0.04, relx=0.135, rely=0.94)


txt_Pot_acionada_msinc = ctk.CTkLabel(frame_MSinc, text="Potência Acionada", anchor="w", font=font_msinc)
txt_Pot_acionada_msinc.place(relwidth=0.1, relheight=0.04, relx=0.2, rely=0.82)
input_Pot_acionada_msinc = ctk.CTkEntry(frame_MSinc, justify='center', font=font_input_msinc)
input_Pot_acionada_msinc.place(relwidth=0.03, relheight=0.04, relx=0.29, rely=0.82)
txt_Pot_acionada_msinc_unit = ctk.CTkLabel(frame_MSinc, text="(HP)", font=font_msinc)
txt_Pot_acionada_msinc_unit.place(relwidth=0.02, relheight=0.04, relx=0.325, rely=0.82)


txt_If_msinc = ctk.CTkLabel(frame_MSinc, text="Corrente de Campo", anchor="w", font=font_msinc)
txt_If_msinc.place(relwidth=0.1, relheight=0.04, relx=0.2, rely=0.88)
input_If_msinc = ctk.CTkEntry(frame_MSinc, justify='center', font=font_input_msinc)
input_If_msinc.place(relwidth=0.03, relheight=0.04, relx=0.29, rely=0.88)
txt_If_msinc_unit = ctk.CTkLabel(frame_MSinc, text="(A)", font=font_msinc)
txt_If_msinc_unit.place(relwidth=0.02, relheight=0.04, relx=0.325, rely=0.88)


txt_Xs_msinc = ctk.CTkLabel(frame_MSinc, text="Reantância Síncrona", anchor="w", font=font_msinc)
txt_Xs_msinc.place(relwidth=0.1, relheight=0.04, relx=0.2, rely=0.94)
input_Xs_msinc = ctk.CTkEntry(frame_MSinc, justify='center', font=font_input_msinc)
input_Xs_msinc.place(relwidth=0.03, relheight=0.04, relx=0.29, rely=0.94)
txt_Xs_msinc_unit = ctk.CTkLabel(frame_MSinc, text="(Ω)", font=font_msinc)
txt_Xs_msinc_unit.place(relwidth=0.02, relheight=0.04, relx=0.325, rely=0.94)


txt_FP_msinc = ctk.CTkLabel(frame_MSinc, text="Fator de Potência", anchor="w", font=font_msinc)
txt_FP_msinc.place(relwidth=0.1, relheight=0.04, relx=0.40, rely=0.82)
input_FP_msinc = ctk.CTkEntry(frame_MSinc, justify='center', font=font_input_msinc)
input_FP_msinc.place(relwidth=0.03, relheight=0.04, relx=0.53, rely=0.82)
status_FP_sgmtd = ctk.CTkSegmentedButton(frame_MSinc, values=['Adiantado', 'Atrasado'], selected_color='#1e0046',
                                   selected_hover_color="#420f85")
status_FP_sgmtd.place(relx=0.51, rely=0.785)
status_FP_sgmtd.set('Adiantado')


txt_Prot_msinc = ctk.CTkLabel(frame_MSinc, text="Perdas p/ Atrito e Ventilação", anchor="w", font=font_msinc)
txt_Prot_msinc.place(relwidth=0.15, relheight=0.04, relx=0.40, rely=0.88)
input_Prot_msinc = ctk.CTkEntry(frame_MSinc, justify='center', font=font_input_msinc)
input_Prot_msinc.place(relwidth=0.03, relheight=0.04, relx=0.53, rely=0.88)
txt_Prot_msinc_unit = ctk.CTkLabel(frame_MSinc, text="(W)", font=font_msinc)
txt_Prot_msinc_unit.place(relwidth=0.02, relheight=0.04, relx=0.565, rely=0.88)


txt_Pnuc_msinc = ctk.CTkLabel(frame_MSinc, text="Perdas no Núcleo", anchor="w", font=font_msinc)
txt_Pnuc_msinc.place(relwidth=0.1, relheight=0.04, relx=0.40, rely=0.94)
input_Pnuc_msinc = ctk.CTkEntry(frame_MSinc, justify='center', font=font_input_msinc)
input_Pnuc_msinc.place(relwidth=0.03, relheight=0.04, relx=0.53, rely=0.94)
txt_Pnuc_msinc_unit = ctk.CTkLabel(frame_MSinc, text="(W)", font=font_msinc)
txt_Pnuc_msinc_unit.place(relwidth=0.02, relheight=0.04, relx=0.565, rely=0.94)

show_Frame(frame_MIT)

app.mainloop()