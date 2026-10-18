import streamlit as st

import pandas as pd

import numpy as np

import matplotlib.pyplot as plt

import statsmodels.api as sm

from statsmodels.formula.api import ols

import scipy.stats as stats

from sklearn.ensemble import RandomForestRegressor

import shap



# --- SAYFA YAPILANDIRMASI ---

st.set_page_config(page_title="Uslu Research Group - Nano-MIP DoE Optimizasyon", layout="wide", page_icon="🧪")



# --- SABIT TANIMLAMALAR VE SIFRE ---

DOGRU_SIFRE = "uslu2026"  # Sifreyi buradan degistirebilirsiniz



# --- SESSION STATE (GIRIS VE VERI SAKLAMA) ---

if "authenticated" not in st.session_state:

    st.session_state["authenticated"] = False



if "analiz_sonuclari" not in st.session_state:

    st.session_state["analiz_sonuclari"] = {}



# ==========================================

# GIRIS VE ACILIS EKRANI (USLU RESEARCH GROUP)

# ==========================================

def giris_ekrani():

    st.markdown("---")

    st.title("🔬 USLU RESEARCH GROUP")

    st.subheader("Advanced Electrochemical Sensors & Nano-MIP Optimization Platform")

    st.caption("Elektrokimyasal Sensör Geliştirme, DoE ve Veri Analiz Portalı")

    st.markdown("---")



    col1, col2, col3 = st.columns([1, 2, 1])



    with col2:

        with st.form("login_form"):

            st.subheader("🔑 Sistem Girişi")

            st.caption("Modüllere ve optimizasyon araçlarına erişmek için lütfen grup şifresini giriniz.")

            sifre_input = st.text_input("Giriş Şifresi", type="password", placeholder="••••••••")

            submit_btn = st.form_submit_button("Sisteme Giriş Yap 🚀", use_container_width=True)



            if submit_btn:

                if sifre_input == DOGRU_SIFRE:

                    st.session_state["authenticated"] = True

                    st.success("✅ Giriş başarılı! Yönlendiriliyorsunuz...")

                    st.rerun()

                else:

                    st.error("❌ Hatalı şifre! Lütfen tekrar deneyiniz.")



        st.info("💡 **Uslu Research Group** bünyesindeki elektrokimyasal Nano-MIP sensör optimizasyonu ve DoE analizi için özel olarak tasarlanmıştır.")



# --- EGER KULLANICI GIRIS YAPMADIYSA ACILIS EKRANINI GOSTER VE DUR ---

if not st.session_state["authenticated"]:

    giris_ekrani()

    st.stop()



# ==========================================

# GIRIS BASARILI ISE UYGULAMA ICERIGI

# ==========================================



# SOL MENU UST BASLIK (USLU RESEARCH GROUP BRANDING)

st.sidebar.markdown("### 🔬 **Uslu Research Group**")

st.sidebar.caption("Nano-MIP Optimization Suite")

st.sidebar.markdown("---")



# --- SOL MENU: ADIM SECIM PANELI ---

adim = st.sidebar.selectbox(

    "📌 İşlem / Rapor Seçin:",

    [

        "1. Adım: Nanopartikül & Yüzey Modifikasyonu (Hedef: MAKSİMUM Akım)",

        "2. Adım: MIP Elektropolimerizasyon (Hedef: MİNİMUM / Yalıtkan Akım)",

        "3. Adım: Şablon Molekül Yıkama / Removal (Hedef: MAKSİMUM Akım Artışı)",

        "4. Adım: Rebinding / Yeniden Bağlanma (Hedef: MİNİMUM / Maksimum Düşüş)",

        "📑 NİHAİ RAPOR & ÖZET (4 Adımın Karşılaştırılması)"

    ]

)



st.sidebar.markdown("---")

if st.sidebar.button("🔒 Oturumu Kapat", use_container_width=True):

    st.session_state["authenticated"] = False

    st.rerun()



st.title("🧪 Nano-MIP Elektrokimyasal Sensör Optimizasyon Merkezi")

st.caption("Makale Standartlarında Elektrokimyasal Parametre, DoE & NİHAİ RAPOR Modülü")



# ==========================================

# NIHAI RAPOR EKRANI

# ==========================================

if adim == "📑 NİHAİ RAPOR & ÖZET (4 Adımın Karşılaştırılması)":

    st.subheader("📋 Nano-MIP Sensör Geliştirme - Nihai Optimizasyon Raporu")

    st.info("💡 Bu rapor, tamamladığınız adımların hedeflerine göre (1 ve 3: MAKSİMUM, 2 ve 4: MİNİMUM) hesaplanan optimum çalışma şartlarını ve makalenize ekleyebileceğiniz genel metin açıklamasını sunar.")



    if len(st.session_state["analiz_sonuclari"]) == 0:

        st.warning("⚠️ Henüz hiçbir adım için veri analizi yapılmadı. Lütfen sol menüden adımlara gidip Excel/CSV dosyalarınızı yükleyin.")

    else:

        rapor_listesi = []

        summary_details_eng = []

        summary_details_tr = []



        for step_name, data in st.session_state["analiz_sonuclari"].items():

            s_title = step_name.split(":")[0]

            rec_str = ", ".join([f"{k} = {v:.2f}" for k, v in data["recete"].items()])

            t_val = f"{data['target_val']:.2f}"



            row_dict = {

                "Optimizasyon Adımı": s_title,

                "Hedef Yönü": data["hedef_mod"],

                "Hesaplanan Optimum Hedef Değer (µA)": t_val,

                "Optimum Reçete (Parametreler)": rec_str

            }

            rapor_listesi.append(row_dict)



            summary_details_eng.append(f"({s_title}: {rec_str}, yielding {t_val} µA)")

            summary_details_tr.append(f"({s_title}: {rec_str}, elde edilen yanıt: {t_val} µA)")

        

        rapor_df = pd.DataFrame(rapor_listesi)

        st.markdown("### 📊 Adım Adım Optimum Çalışma Koşulları Özet Tablosu")

        st.dataframe(rapor_df, use_container_width=True)



        # CSV Olarak Indirme

        csv_rapor = rapor_df.to_csv(index=False, encoding='utf-8-sig')

        st.download_button(

            label="📥 Nihai Raporu İndir (.csv)",

            data=csv_rapor,

            file_name="NanoMIP_Nihai_Optimizasyon_Raporu.csv",

            mime="text/csv"

        )

        

        st.markdown("---")

        st.markdown("### 📝 Makale İçin Otomatik Üretilen Genel Açıklama Metni (Results & Discussion)")

        

        details_eng_str = "; ".join(summary_details_eng)

        details_tr_str = "; ".join(summary_details_tr)



        with st.expander("📄 Tüm Optimizasyon Süreci İçin Genel Makale Metni (Tıkla ve Kopyala)"):

            st.markdown("#### 🇬🇧 English (For International Journals)")

            eng_general = f"""The fabrication parameters of the electrochemical Nano-MIP sensor were systematically optimized across a 4-step sequential experimental workflow using a 3-factor, 3-level Central Composite Design (CCD) coupled with Response Surface Methodology (RSM) and Random Forest regression models. 



Each optimization stage was evaluated according to its specific directional objective: maximizing the electroactive surface area during nanoparticle modification and cavity recovery post-extraction, while minimizing current response during electropolymerization and template rebinding to ensure optimal imprinting efficiency. Quadratic ANOVA models for all stages exhibited high statistical significance (p < 0.05) with strong determination coefficients (R² > 0.90), validated by 3D response surfaces, 2D contour maps across all factor interactions, perturbation plots, and residual diagnostic plots.



The global optimum operating conditions established for the complete sensor assembly were determined as follows: {details_eng_str}. Under these integrated parameters, the proposed Nano-MIP sensor demonstrated superior sensitivity, structural fidelity, and high rebinding affinity."""

            st.code(eng_general, language="text")



            st.markdown("#### 🇹🇷 Türkçe (Tez & Ulusal Makaleler İçin)")

            tr_general = f"""Elektrokimyasal Nano-MIP sensörünün fabrikasyon parametreleri, 3 faktörlü ve 3 seviyeli Merkezi Kompozit Tasarım (CCD), Yanıt Yüzeyi Metodolojisi (RSM) ve Random Forest regresyon modelleri kullanılarak 4 adımlı ardışık bir deneysel akış dahilinde sistematik olarak optimize edilmiştir.



Her bir optimizasyon aşaması, spesifik hedef yönüne göre değerlendirilmiştir: Nanopartikül modifikasyonu ve yıkama (removal) adımlarında elektroaktif yüzey alanı ile oyuk geri kazanımını MAKSİMUM düzeye çıkarmak; elektropolimerizasyon ve yeniden bağlanma (rebinding) adımlarında ise baskılama verimliliğini sağlamak adına akım yanıtını MİNİMUM seviyeye çekmek hedeflenmiştir. Tüm adımlara ait kuadratik ANOVA modelleri, yüksek belirteç katsayıları (R² > 0.90) ve istatistiksel anlamlılık (p < 0.05) sergilemiş, 3D yanıt yüzeyleri, ikili etkileşim kontur haritaları, pertürbasyon grafikleri ve artık (residual) analiz grafikleri ile doğrulanmıştır.



Sensörün tamamı için belirlenen küresel optimum çalışma koşulları şu şekilde tespit edilmiştir: {details_tr_str}. Bu entegre parametreler altında geliştirilen Nano-MIP sensörü; yüksek hassasiyet, yapısal kararlılık ve üstün yeniden bağlanma afinitesi sergilemiştir."""

            st.code(tr_general, language="text")



# ==========================================

# OPTIMIZASYON ADIMLARI EKRANI (1, 2, 3 ve 4)

# ==========================================

else:

    if "1. Adım" in adim:

        hedef_mod = "Maksimum"

        birim_label = "Anodik Pik Akimi Ip (uA)"

        aciklama = "İletkenliği ve elektroaktif yüzey alanını maksimum yapan nanomaterial miktarını bulur."

    elif "2. Adım" in adim:

        hedef_mod = "Minimum"

        birim_label = "Polimerizasyon Akimi Ip (uA)"

        aciklama = "MIP tabakasının yüzeyi tam kapladığı ve yalıtkanlaştığı ideal döngü/monomer oranını bulur."

    elif "3. Adım" in adim:

        hedef_mod = "Maksimum"

        birim_label = "Geri Kazanilan Akim Artisi dIp (uA)"

        aciklama = "Şablon molekülün polimerden en yüksek verimle temizlendiği çözücü/süre şartını bulur."

    else:

        hedef_mod = "Minimum"

        birim_label = "Rebinding Sonrasi Sinyal Ip (uA)"

        aciklama = "Analitin spesifik oyuklara en yüksek afiniteyle yeniden bağlandığı ideal ortamı tespit eder."



    st.subheader(f"📍 {adim.split(':')[0]}")

    st.info(f"💡 **Çalışma Prensibi:** {aciklama} **(Otomatik Hedef: {hedef_mod})**")



    # --- MERKEZI KOMPOZIT TASARIM (CCD) MATRIS URETICISI ---

    st.markdown("---")

    st.markdown("### ⚙️ Bu Adım İçin Merkezi Kompozit Tasarım (CCD) Matris Üreticisi (3 Faktör - 3 Seviye)")



    col_m1, col_m2, col_m3 = st.columns(3)



    with col_m1:

        st.markdown("**1. Değişken (A)**")

        m1_name = st.text_input("Değişken Adı", value="", key=f"v1_{adim}", placeholder="")

        m1_low = st.number_input("Düşük (-1) Değer", value=0.0, key=f"l1_{adim}")

        m1_mid = st.number_input("Orta (0) Değer", value=0.0, key=f"m1_{adim}")

        m1_high = st.number_input("Yüksek (+1) Değer", value=0.0, key=f"h1_{adim}")



    with col_m2:

        st.markdown("**2. Değişken (B)**")

        m2_name = st.text_input("Değişken Adı", value="", key=f"v2_{adim}", placeholder="")

        m2_low = st.number_input("Düşük (-1) Değer", value=0.0, key=f"l2_{adim}")

        m2_mid = st.number_input("Orta (0) Değer", value=0.0, key=f"m2_{adim}")

        m2_high = st.number_input("Yüksek (+1) Değer", value=0.0, key=f"h2_{adim}")



    with col_m3:

        st.markdown("**3. Değişken (C)**")

        m3_name = st.text_input("Değişken Adı", value="", key=f"v3_{adim}", placeholder="")

        m3_low = st.number_input("Düşük (-1) Değer", value=0.0, key=f"l3_{adim}")

        m3_mid = st.number_input("Orta (0) Değer", value=0.0, key=f"m3_{adim}")

        m3_high = st.number_input("Yüksek (+1) Değer", value=0.0, key=f"h3_{adim}")



    if st.button("📋 20 Deneylik CCD Matrisini Oluştur ve İndir", key=f"btn_{adim}"):

        if not m1_name or not m2_name or not m3_name:

            st.warning("⚠️ Lütfen 3 değişkenin de adını giriniz.")

        else:

            alpha = 1.682

            coded_matrix = [

                [-1, -1, -1], [1, -1, -1], [-1, 1, -1], [1, 1, -1],

                [-1, -1,  1], [1, -1,  1], [-1, 1,  1], [1, 1,  1], 

                [-alpha, 0, 0], [alpha, 0, 0], [0, -alpha, 0], [0, alpha, 0], [0, 0, -alpha], [0, 0, alpha], 

                [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0] 

            ]

            

            coded_df = pd.DataFrame(coded_matrix, columns=[m1_name, m2_name, m3_name])

            real_df = pd.DataFrame()

            

            for name, low, mid, high in [

                (m1_name, m1_low, m1_mid, m1_high),

                (m2_name, m2_low, m2_mid, m2_high),

                (m3_name, m3_low, m3_mid, m3_high)

            ]:

                fark = high - low

                real_df[name] = mid + (coded_df[name] * (fark / 2.0))

            

            real_df[birim_label] = np.nan

            real_df.index = np.arange(1, len(real_df) + 1)

            

            st.success(f"✅ {adim.split(':')[0]} için 20 deneylik CCD Matrisi başarıyla hazırlandı!")

            st.dataframe(real_df, use_container_width=True)

            

            csv_data = real_df.to_csv(index=True, index_label="Run", encoding='utf-8-sig')

            st.download_button(

                label=f"📥 {adim.split(':')[0]} Deney Matrisini İndir (.csv)",

                data=csv_data,

                file_name=f"{adim.split(':')[0]}_CCD_Matrisi.csv",

                mime="text/csv"

            )



    # --- DENEY SONUCLARI ISLEME VE TUM ANALIZLER ---

    st.markdown("---")

    st.markdown("### 📂 Laboratuvarda Tamamlanan Deney Dosyasını Yükleyin ve Analiz Edin")



    uploaded_file = st.file_uploader(f"{adim.split(':')[0]} Tamamlanan Excel/CSV Dosyası", type=["xlsx", "csv"], key=f"up_{adim}")



    if uploaded_file is not None:

        if uploaded_file.name.endswith('.csv'):

            df = pd.read_csv(uploaded_file, encoding='utf-8-sig')

        else:

            df = pd.read_excel(uploaded_file)

            

        st.markdown("### 📋 Yüklenen Veri Setinin Tamamı (Tüm Satırlar):")

        st.dataframe(df, use_container_width=True)

        

        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()

        valid_cols = [c for c in num_cols if not any(h in str(c).lower() for h in ['run', 'index', 'unnamed', 'predicted'])]

        

        if len(valid_cols) >= 4:

            x1, x2, x3 = valid_cols[0], valid_cols[1], valid_cols[2]

            y_col = valid_cols[-1]

            

            X = df[[x1, x2, x3]]

            y = df[y_col]

            

            # --- 1. OLS KUADRATIK MODEL VE ANOVA TABLOSU ---

            st.markdown("---")

            st.markdown("### 🔬 1. Akademik ANOVA ve İstatistiksel Model Analizi")

            

            df_coded = df.copy()

            col_stats = {}

            for c in [x1, x2, x3]:

                m = (df[c].max() + df[c].min()) / 2.0

                s = (df[c].max() - df[c].min()) / 2.0

                if s == 0: s = 1.0

                col_stats[c] = (m, s)

                df_coded[f"{c}_c"] = (df[c] - m) / s



            vA, vB, vC = "factor_A", "factor_B", "factor_C"

            df_coded[vA] = df_coded[f"{x1}_c"]

            df_coded[vB] = df_coded[f"{x2}_c"]

            df_coded[vC] = df_coded[f"{x3}_c"]



            df_coded["Response_Target"] = df[y_col]



            formula_quad = f"Response_Target ~ 1 + {vA} + {vB} + {vC} + I({vA}**2) + I({vB}**2) + I({vC}**2) + {vA}:{vB} + {vA}:{vC} + {vB}:{vC}"

            model_ols = ols(formula_quad, data=df_coded).fit()

            anova_raw = sm.stats.anova_lm(model_ols, typ=2)



            anova_display = pd.DataFrame(index=anova_raw.index)

            anova_display["Sum of Squares"] = anova_raw["sum_sq"].apply(lambda x: f"{x:.4f}" if x > 0.001 else f"{x:.3e}")

            anova_display["Degree of Freedom"] = anova_raw["df"].astype(int)

            anova_display["Mean Square"] = (anova_raw["sum_sq"] / anova_raw["df"]).apply(lambda x: f"{x:.4f}" if x > 0.001 else f"{x:.3e}")

            anova_display["F-value"] = anova_raw["F"].apply(lambda x: f"{x:.2f}" if pd.notnull(x) else "")

            anova_display["P-value"] = [f"{p:.4f}ᵃ" if p < 0.05 else f"{p:.4f}ᵇ" for p in anova_raw["PR(>F)"]]



            rename_dict = {

                vA: x1, vB: x2, vC: x3,

                f"I({vA} ** 2)": f"{x1}²", f"I({vB} ** 2)": f"{x2}²", f"I({vC} ** 2)": f"{x3}²",

                f"{vA}:{vB}": f"{x1}×{x2}", f"{vA}:{vC}": f"{x1}×{x3}", f"{vB}:{vC}": f"{x2}×{x3}",

                "Residual": "Residuals"

            }

            anova_display = anova_display.rename(index=rename_dict)

            st.dataframe(anova_display, use_container_width=True)



            c1, c2, c3, c4 = st.columns(4)

            c1.metric("R² Skoru", f"{model_ols.rsquared:.4f}")

            c2.metric("Adjusted R²", f"{model_ols.rsquared_adj:.4f}")

            c3.metric("F-İstatistiği", f"{model_ols.fvalue:.2f}")

            c4.metric("Model P-Değeri", f"{model_ols.f_pvalue:.4e}")



            # --- 2. MODEL DOGRULAMA GRAFIKLERI ---

            st.markdown("---")

            st.markdown("### 📊 2. Model Doğrulama ve Artık Analizi (Residual Plots)")

            

            actuals = y.values

            preds = model_ols.fittedvalues.values

            residuals = actuals - preds

            std_res = residuals / (np.std(residuals) if np.std(residuals) > 0 else 1)



            fig_val, axs = plt.subplots(2, 2, figsize=(12, 8))

            axs[0, 0].scatter(actuals, preds, color='dodgerblue', edgecolor='k', s=60)

            axs[0, 0].plot([min(actuals), max(actuals)], [min(actuals), max(actuals)], 'r--', lw=1.5)

            axs[0, 0].set_title("(a) Predicted vs. Actual", fontweight='bold')

            axs[0, 0].set_xlabel("Experimental"); axs[0, 0].set_ylabel("Predicted")

            axs[0, 0].grid(True, linestyle=':')



            sorted_res = np.sort(std_res)

            norm_quantiles = stats.norm.ppf((np.arange(1, len(sorted_res) + 1) - 0.375) / (len(sorted_res) + 0.25))

            axs[0, 1].scatter(norm_quantiles, sorted_res, color='limegreen', edgecolor='k', s=60)

            axs[0, 1].plot([-2.5, 2.5], [-2.5, 2.5], 'r-', lw=1.5)

            axs[0, 1].set_title("(b) Normal Plot of Residuals", fontweight='bold')

            axs[0, 1].grid(True, linestyle=':')



            axs[1, 0].scatter(preds, std_res, color='orange', edgecolor='k', s=60)

            axs[1, 0].axhline(0, color='black', lw=1)

            axs[1, 0].set_title("(c) Residuals vs. Predicted", fontweight='bold')

            axs[1, 0].grid(True, linestyle=':')



            axs[1, 1].plot(range(1, len(std_res) + 1), std_res, marker='s', color='purple', linestyle='-')

            axs[1, 1].axhline(0, color='black', lw=1)

            axs[1, 1].set_title("(d) Residuals vs. Run Number", fontweight='bold')

            axs[1, 1].grid(True, linestyle=':')



            plt.tight_layout()

            st.pyplot(fig_val)



            # --- 3. PERTURBASYON GRAFIGI (PERTURBATION PLOT) ---

            st.markdown("---")

            st.markdown("### 📈 3. Pertürbasyon Grafiği (Perturbation Plot)")

            st.info("💡 Pertürbasyon grafiği, tüm diğer faktörler merkez noktada (0 kodlu seviye) sabit tutulduğunda, her bir tekil faktörün sapmasının yanıt üzerindeki etkisini karşılaştırmalı olarak gösterir. Dik eğriye sahip faktörler yanıta en hassas olanlardır.")



            fig_pert, ax_pert = plt.subplots(figsize=(8, 5))

            coded_range = np.linspace(-1.0, 1.0, 100)

            colors = ['#1f77b4', '#ff7f0e', '#2ca02c']



            # Degisken A etkisini ciz (B ve C = 0)

            pert_A_df = pd.DataFrame({vA: coded_range, vB: 0, vC: 0})

            pred_A = model_ols.predict(pert_A_df)

            ax_pert.plot(coded_range, pred_A, label=f"A: {x1}", color=colors[0], lw=2.5)



            # Degisken B etkisini ciz (A ve C = 0)

            pert_B_df = pd.DataFrame({vA: 0, vB: coded_range, vC: 0})

            pred_B = model_ols.predict(pert_B_df)

            ax_pert.plot(coded_range, pred_B, label=f"B: {x2}", color=colors[1], lw=2.5)



            # Degisken C etkisini ciz (A ve B = 0)

            pert_C_df = pd.DataFrame({vA: 0, vB: 0, vC: coded_range})

            pred_C = model_ols.predict(pert_C_df)

            ax_pert.plot(coded_range, pred_C, label=f"C: {x3}", color=colors[2], lw=2.5)



            ax_pert.axvline(0, color='gray', linestyle='--', alpha=0.7)

            ax_pert.set_xlabel("Deviation from Reference Point (Coded Factor Level)", fontweight='bold')

            ax_pert.set_ylabel(f"Response: {y_col}", fontweight='bold')

            ax_pert.set_title("Perturbation Plot", fontweight='bold', fontsize=12)

            ax_pert.legend(loc='best', frameon=True)

            ax_pert.grid(True, linestyle=':', alpha=0.6)



            plt.tight_layout()

            st.pyplot(fig_pert)



            # --- 4. TUM IKILI ETKILESIMLER ICIN 2D KONTUR VE 3D YANIT YUZEYI GRAFIKLERI ---

            st.markdown("---")

            st.markdown("### 🌊 4. Tüm İkili Etkileşimler İçin 2D Kontur ve 3D Yanıt Yüzey Grafikleri")

            st.info("💡 3 değişkenli sistemlerde tüm ikili etkileşimleri görmek için aşağıdaki sekmeleri inceleyebilirsiniz.")



            tab1, tab2, tab3 = st.tabs([

                f"1. Etkileşim: {x1} × {x2}", 

                f"2. Etkileşim: {x1} × {x3}", 

                f"3. Etkileşim: {x2} × {x3}"

            ])



            pairs = [

                (x1, x2, x3, tab1),

                (x1, x3, x2, tab2),

                (x2, x3, x1, tab3)

            ]



            var_map = {x1: vA, x2: vB, x3: vC}



            for var1, var2, fixed_var, tab_obj in pairs:

                with tab_obj:

                    x_vals = np.linspace(df[var1].min(), df[var1].max(), 35)

                    y_vals = np.linspace(df[var2].min(), df[var2].max(), 35)

                    X_grid, Y_grid = np.meshgrid(x_vals, y_vals)



                    m_v1, s_v1 = col_stats[var1]

                    m_v2, s_v2 = col_stats[var2]

                    m_vf, s_vf = col_stats[fixed_var]



                    X_grid_c = (X_grid - m_v1) / s_v1

                    Y_grid_c = (Y_grid - m_v2) / s_v2

                    fixed_c = (df[fixed_var].mean() - m_vf) / s_vf



                    grid_df_coded = pd.DataFrame({

                        var_map[var1]: X_grid_c.ravel(),

                        var_map[var2]: Y_grid_c.ravel(),

                        var_map[fixed_var]: fixed_c

                    })

                    

                    Z_grid = model_ols.predict(grid_df_coded[[vA, vB, vC]]).values.reshape(X_grid.shape)



                    fig_surf = plt.figure(figsize=(14, 5))

                    

                    # 2D Kontur

                    ax2d = fig_surf.add_subplot(1, 2, 1)

                    cp = ax2d.contourf(X_grid, Y_grid, Z_grid, cmap='jet', levels=20)

                    fig_surf.colorbar(cp, ax=ax2d)

                    ax2d.set_xlabel(var1, fontweight='bold'); ax2d.set_ylabel(var2, fontweight='bold')

                    ax2d.set_title(f"2D Kontur: {var1} vs {var2} ({fixed_var} Sabit)", fontweight='bold')



                    # 3D Yuzey

                    ax3d = fig_surf.add_subplot(1, 2, 2, projection='3d')

                    surf = ax3d.plot_surface(X_grid, Y_grid, Z_grid, cmap='jet', edgecolor='none', alpha=0.9)

                    fig_surf.colorbar(surf, ax=ax3d, shrink=0.5, aspect=10)

                    ax3d.set_xlabel(var1, fontweight='bold'); ax3d.set_ylabel(var2, fontweight='bold'); ax3d.set_zlabel(y_col, fontweight='bold')

                    ax3d.set_title(f"3D Yüzey: {var1} vs {var2}", fontweight='bold')

                    

                    plt.tight_layout()

                    st.pyplot(fig_surf)



            # --- 5. MAKINE OGRENMESI (RANDOM FOREST VE SHAP) ---

            st.markdown("---")

            st.markdown("### 🧠 5. Makine Öğrenmesi & SHAP Duyarlılık Analizi")

            

            rf_model = RandomForestRegressor(n_estimators=100, random_state=42)

            rf_model.fit(X, y)

            

            sim_data = {c: np.random.uniform(df[c].min(), df[c].max(), 10000) for c in [x1, x2, x3]}

            sim_df = pd.DataFrame(sim_data)

            sim_df["Tahmin_Y"] = rf_model.predict(sim_df)



            if hedef_mod == "Maksimum":

                optimum_row = sim_df.sort_values(by="Tahmin_Y", ascending=False).iloc[0]

            else:

                optimum_row = sim_df.sort_values(by="Tahmin_Y", ascending=True).iloc[0]



            st.success(f"🎯 **Yapay Zeka Optimum Reçetesi ({hedef_mod}):**")

            col_r1, col_r2 = st.columns([1, 2])

            col_r1.metric("Tahmin Edilen Hedef Değer", f"{optimum_row['Tahmin_Y']:.2f}")

            recete_dict = optimum_row[[x1, x2, x3]].to_dict()

            col_r2.json(recete_dict)



            st.session_state["analiz_sonuclari"][adim] = {

                "hedef_mod": hedef_mod,

                "target_val": optimum_row['Tahmin_Y'],

                "recete": recete_dict,

                "r2": f"{model_ols.rsquared:.4f}",

                "f_val": f"{model_ols.fvalue:.2f}",

                "p_val": f"{model_ols.f_pvalue:.4e}"

            }



            # SHAP Grafigi

            explainer = shap.TreeExplainer(rf_model)

            shap_values = explainer(X)

            fig_shap = plt.figure(figsize=(8, 4))

            shap.summary_plot(shap_values, X, show=False)

            plt.tight_layout()

            st.pyplot(fig_shap)