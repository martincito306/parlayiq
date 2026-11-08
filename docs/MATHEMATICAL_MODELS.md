# PARLAYIQ — Especificación de Modelos Matemáticos y Cuantitativos

Este documento formaliza las bases matemáticas implementadas en el motor cuantitativo de **PARLAYIQ** (`backend/app/engine`).

---

## 1. Distribución de Poisson y Modelo Dixon-Coles

Para eventos de goles de baja frecuencia, modelamos los goles locales ($X$) y visitantes ($Y$) con medias de ataque y defensa:
$$\lambda = \alpha_{\text{home}} \cdot \beta_{\text{away}} \cdot \gamma_{\text{home\_adv}}$$
$$\mu = \alpha_{\text{away}} \cdot \beta_{\text{home}}$$

### Corrección Dixon-Coles para Marcadores Bajos
La distribución de Poisson estándar subestima los empates 0-0 y marcadores 1-0, 0-1, 1-1. Se aplica el factor de corrección $\tau(x, y)$:
$$\tau(x, y) = \begin{cases} 
1 - \lambda \mu \rho & \text{si } x = 0, y = 0 \\
1 + \lambda \rho & \text{si } x = 0, y = 1 \\
1 + \mu \rho & \text{si } x = 1, y = 0 \\
1 - \rho & \text{si } x = 1, y = 1 \\
1 & \text{en cualquier otro caso}
\end{cases}$$
Donde $\rho$ es el parámetro de correlación empírica de goles.
$$P(X=x, Y=y) = \tau(x, y) \cdot \frac{e^{-\lambda}\lambda^x}{x!} \cdot \frac{e^{-\mu}\mu^y}{y!}$$

---

## 2. Distribución Binomial Negativa (Sobredispersión)

Eventos como **tiros de jugadores, córners y tarjetas** presentan sobredispersión ($\text{Var}(X) > \mathbb{E}[X]$), violando el supuesto de Poisson.
Se parametriza la Binomial Negativa mediante la media $\mu$ y el parámetro de dispersión $r$:
$$P(X = k) = \binom{k + r - 1}{k} \left(\frac{r}{r + \mu}\right)^r \left(\frac{\mu}{r + \mu}\right)^k$$
Donde $r = \frac{\mu^2}{\sigma^2 - \mu}$.

---

## 3. Modelado de Rendimiento de Jugadores (Player Props)

La probabilidad de que un jugador supere una línea de disparos $k$ (ej. Más de 1.5 disparos a puerta) depende de:
1. **Minutos proyectados**: $\phi = \frac{\text{Minutos Esperados}}{90}$
2. **Promedio por 90 ajustado**: $\lambda_{90} = \bar{X}_{90} \times \text{Factor}_{\text{Rival\_Def}} \times \text{Factor}_{\text{Localía}}$
3. **Lambda efectivo**: $\lambda_{\text{eff}} = \lambda_{90} \cdot \phi$
4. **Probabilidad acumulada inversa**: $P(X \ge \text{Línea}) = 1 - \sum_{j=0}^{\lfloor \text{Línea} \rfloor} P(X = j \mid \lambda_{\text{eff}}, r)$

---

## 4. Matrices de Correlación y Cópula Gaussiana para Same Game Parlay (SGP)

Nunca se deben multiplicar ingenuamente probabilidades de un mismo partido (ej. Más de 2.5 goles y Más de 9.5 córners y Delantero marca).
1. Se estima la **matriz de covarianza / correlación** empírica $R$ entre mercados.
2. Se generan vectores uniformes correlacionados mediante una cópula Gaussiana:
   $$Z \sim \mathcal{N}(0, R) \implies U_i = \Phi(Z_i)$$
3. Se transforman a las marginales de cada evento mediante la función cuantil acumulada inversa ($F_i^{-1}(U_i)$).
4. Se ejecutan $N = 10.000$ iteraciones vectorizadas en NumPy.
5. La probabilidad conjunta calibrada es:
   $$P_{\text{joint}} = \frac{1}{N} \sum_{m=1}^N \prod_{i=1}^M \mathbb{I}(\text{Evento}_i \text{ cumplido en simulación } m)$$

---

## 5. Pricing, Overround y Valor Esperado (EV)

- **Cuota Justa (Fair Odds)**:
  $$\text{Cuota}_{\text{Justa}} = \frac{1}{P_{\text{estimada}}}$$
- **Probabilidad Implícita del Mercado**:
  $$P_{\text{implícita}} = \frac{1}{\text{Cuota}_{\text{Mercado}}}$$
- **Valor Esperado (EV)**:
  $$\text{EV} = (P_{\text{estimada}} \times \text{Cuota}_{\text{Mercado}}) - 1$$
  - Si $\text{EV} > 0$: **Apuesta de Valor** (Edge positivo).
  - Si $\text{EV} \le 0$: Valor desfavorable, castigado por el margen de la casa (Vig/Overround).
- **Criterio de Kelly Fraccional (Money Management)**:
  $$f^* = \frac{P \cdot b - (1 - P)}{b} \times \text{Fraction}_{\text{safe}} \quad (b = \text{Cuota} - 1)$$

---

## 6. Calibración y Auditoría Histórica

- **Brier Score**:
  $$BS = \frac{1}{N} \sum_{i=1}^N (P_i - y_i)^2 \quad (y_i \in \{0, 1\})$$
  *(Un valor cercano a 0 indica alta calibración; 0.25 es adivinación aleatoria para eventos binarios 50/50)*.
- **Expected Calibration Error (ECE)**:
  Calculado agrupando predicciones en $B = 10$ bins de confianza y comparando precisión observada vs confianza media predicha.
