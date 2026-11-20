import streamlit as st
import sqlite3
import argon2
import streamlit as st
import streamlit.components.v1 as components

# Configuración de la base de datos
session_state = st.session_state

# Configuración de la base de datos
conn = sqlite3.connect('a_la_par.db', check_same_thread=False)
c = conn.cursor()

# Inicializar la sesión
if 'logged_in' not in session_state:
    session_state.logged_in = False
    session_state.user_id = None

# Componentes personalizados
def estilo_personalizado():
    st.markdown(
        """
        <style>
        .sidebar .sidebar-content {
            background-color: #F0F8FF;
        }
        .stButton>button {
            color: #ffffff;
            background-color: #00008B;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Configuración de la interfaz Streamlit
st.set_page_config(page_title="A la Par", layout="wide")

# Función para crear la estructura de las tablas
def crear_tablas():
    c.execute('''
        CREATE TABLE IF NOT EXISTS materiales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            contenido TEXT,
            objetivo TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            descripcion TEXT,
            fecha_entrega DATE,
            material_vinculado INTEGER,
            FOREIGN KEY(material_vinculado) REFERENCES materiales(id)
        )
    ''')
    conn.commit()

# Función para manejar el login
def iniciar_sesion(email, password):
    c.execute("SELECT id, password_hash FROM usuarios WHERE email = ?", (email,))
    user = c.fetchone()
    if user and argon2.PasswordHasher().verify(user[1], password):
        session_state.logged_in = True
        session_state.user_id = user[0]

# Función para manejar el registro
def registro_usuario(nombre, email, password):
    password_hash = argon2.PasswordHasher().hash(password)
    c.execute("INSERT INTO usuarios (nombre, email, password_hash) VALUES (?, ?, ?)", 
              (nombre, email, password_hash))
    conn.commit()
    
# Crear las tablas
c.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        email TEXT UNIQUE,
        password_hash TEXT
    )
''')
crear_tablas()

# Navegación
if not session_state.logged_in:
    st.sidebar.title("A la Par")
    menu = ["Espacio de aprendizaje", "Panel"]
    choice = st.sidebar.radio("", menu, index=0)

    st.sidebar.markdown(
        f"""
        <style>
        .sidebar .{choice.replace(" ", "-").lower()} {{
            background-color: #E0F8FF;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
    st.sidebar.markdown('\n'.join([f'<div class="{item.replace(" ", "-").lower()}">{item}</div>' for item in menu]), unsafe_allow_html=True)
    if choice == "Iniciar sesión":
        st.subheader("Iniciar sesión")
        email = st.text_input("Correo", "")
        password = st.text_input("Contraseña", type="password")
        
        if st.button("Iniciar sesión"):
            iniciar_sesion(email, password)
            if session_state.logged_in:
                st.success("Sesión iniciada correctamente")
            else:
                st.error("Correo o contraseña incorrectos")
    elif choice == "Crear cuenta":
        st.subheader("Crear cuenta")
        nombre = st.text_input("Nombre completo", "")
        email = st.text_input("Correo", "")
        password = st.text_input("Contraseña", type="password")
        confirm_password = st.text_input("Confirmar contraseña", type="password")
        
        if st.button("Registrar"):
            if password == confirm_password:
                try:
                    registro_usuario(nombre, email, password)
                    st.success("Cuenta creada exitosamente")
                except sqlite3.IntegrityError:
                    st.error("El correo ya está registrado")
            else:
                st.error("Las contraseñas no coinciden")

else:
    st.sidebar.title("A la Par")
    st.sidebar.text(f"Bienvenido, Usuario {session_state.user_id}")
    st.sidebar.button("Cerrar sesión", on_click=lambda: st.experimental_rerun())

# Mostrar el estado de sesión en la esquina superior derecha
st.markdown('<div style="background-color: #FFFFFF; border-bottom: 1px solid #E0E0E0; padding: 5px; text-align: right;">', unsafe_allow_html=True)
if not session_state.logged_in:
    st.button("Iniciar sesión", on_click=lambda: session_state.update({"intended_section": seccion}))
else:
    st.write(f"Hola, {session_state.user_id}")
    st.button("Cerrar sesión", on_click=lambda: st.experimental_rerun())
st.markdown(
    """
    <span style="cursor:pointer;" onclick="document.getElementById('account-menu').style.display='block'">&#9776;</span>
    <div id="account-menu" style="display:none;">
      <button onclick="showLogin()">Iniciar sesión</button>
      <button onclick="showRegister()">Registrarse</button>
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown('</div>', unsafe_allow_html=True)

if choice == "Espacio de aprendizaje":
    st.title("Espacio de aprendizaje")

    # Subir archivo
    file = st.file_uploader("Subí tu material", type=["txt", "docx", "pdf"])

    # Escribir el objetivo
    objetivo = st.text_input("¿Qué necesitás poder hacer con este material?", "")

    if file is not None:
        st.write("Revisá el contenido extraído del archivo:")
        # Aquí iría la lógica para extraer el texto del archivo seleccionado
        st.write("**Nombre del archivo:**", file.name)
        st.write("**Tipo de archivo:**", file.type)

    if st.button("Guardar material"):
        st.write("Material y objetivo guardados para procesar más tarde.")
elif choice == "Panel":
    st.title("Panel")
    st.write("Aquí se mostrarán las métricas de usuario.")
    st.write("Datos: cantidad de tareas, material guardado, etc.")
