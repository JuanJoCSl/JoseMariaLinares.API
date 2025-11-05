from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime # Podrías necesitar instalar esta librería (pip install pytz)
import sqlite3
from datetime import datetime
import os
import hashlib  # Para cifrar contraseñas

app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas las rutas

DATABASE = 'comunicados.db'

def get_db_connection():
    """Establece conexión con la base de datos SQLite"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    """Cifra la contraseña usando SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    """Inicializa la base de datos con todas las tablas necesarias"""
    conn = get_db_connection()
    
    # Tabla comunicados
    conn.execute('''
        CREATE TABLE IF NOT EXISTS comunicados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            contenido TEXT NOT NULL,
            imagen TEXT,
            fecha TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    
    # Tabla blog
    conn.execute('''
        CREATE TABLE IF NOT EXISTS blog (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            contenido TEXT NOT NULL,
            categoria TEXT NOT NULL,
            imagen TEXT,
            fecha TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    
    # Tabla comentarios
    conn.execute('''
        CREATE TABLE IF NOT EXISTS comentarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            contenido TEXT NOT NULL,
            imagen TEXT,
            fecha TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    
    # Tabla deportes
    conn.execute('''
        CREATE TABLE IF NOT EXISTS deportes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            contenido TEXT NOT NULL,
            imagen TEXT,
            fecha TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    # Tabla horarios
    conn.execute('''
        CREATE TABLE IF NOT EXISTS horarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            imagen TEXT,
            fecha TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')

    conn.execute('''
    CREATE TABLE IF NOT EXISTS profesores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        cargo TEXT NOT NULL,
        area TEXT NOT NULL,
        especialidad TEXT NOT NULL,
        numero_celular TEXT NOT NULL,
        url_foto TEXT,
        created_at TEXT NOT NULL
        )
    ''')

    # NUEVA TABLA: usuarios
    conn.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            password TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    
    # Insertar datos de ejemplo si las tablas están vacías
    for table in ['comunicados', 'blog', 'comentarios', 'deportes', 'horarios', 'profesores', 'usuarios']:
        count = conn.execute(f'SELECT COUNT(*) as count FROM {table}').fetchone()['count']
        if count == 0:
            if table == 'comunicados':
                conn.execute('''
                    INSERT INTO comunicados (titulo, contenido, imagen, fecha, created_at)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    'Desfile del Kinder José Antonio Zampa',
                    'Se convoca a la banda, la promoción y docentes del colegio a asistir al desfile del aniversario del Kinder José Antonio Zampa.',
                    '../img/com.png',
                    '2025-09-01',
                    datetime.utcnow().isoformat() + 'Z'
                ))
                conn.execute('''
                    INSERT INTO comunicados (titulo, contenido, imagen, fecha, created_at)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    'Entrada el dia viernes 4 de septiembre Acto Cívico a Jose Antonio Zampa',
                    'Se convoca a la banda, la promoción y docentes del colegio a asistir al desfile del aniversario del Kinder José Antonio Zampa.',
                    '../img/comm.png',
                    '2025-09-01',
                    datetime.utcnow().isoformat() + 'Z'
                ))
            elif table == 'blog':
                conn.execute('''
                    INSERT INTO blog (titulo, contenido, categoria, imagen, fecha, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                    '¡Campeones del Torneo!',
                    'Resumen de la emocionante final de fútbol sala.',
                    'Deportes',
                    '../img/ejercicio.avif',
                    '2025-10-15',
                    datetime.utcnow().isoformat() + 'Z'
                ))
                conn.execute('''
                    INSERT INTO blog (titulo, contenido, categoria, imagen, fecha, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                    '¡Feria de Ciencias 2025',
                    'Los proyectos más innovadores de este año escolar que demuestran la creatividad y conocimiento científico de nuestros alumnos.',
                    'Ciencia',
                    '../img/ciencia.avif',
                    '2025-10-15',
                    datetime.utcnow().isoformat() + 'Z'
                ))
                conn.execute('''
                    INSERT INTO blog (titulo, contenido, categoria, imagen, fecha, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                    '¡Nuestra Gran Banda',
                    'Conozca a los músicos que nos representan con orgullo en cada evento y celebración de nuestra comunidad educativa.',
                    'Música',
                    '../img/ciencia.avif',
                    '2025-10-15',
                    datetime.utcnow().isoformat() + 'Z'
                ))
            elif table == 'comentarios':
                conn.execute('''
                    INSERT INTO comentarios (titulo, contenido, imagen, fecha, created_at)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    'Padre de Familia',
                    'El colegio José María Linares tiene una gran banda. La dedicación de los estudiantes y maestros es realmente admirable.',
                    '',
                    '2025-10-18',
                    datetime.utcnow().isoformat() + 'Z'
                ))
                conn.execute('''
                    INSERT INTO comentarios (titulo, contenido, imagen, fecha, created_at)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    'Exalumno',
                    '"Los estudiantes del colegio son los mejores. Siempre demuestran valores y excelencia académica en cada actividad."',
                    '',
                    '2025-10-18',
                    datetime.utcnow().isoformat() + 'Z'
                ))
            elif table == 'deportes':
                conn.execute('''
                    INSERT INTO deportes (titulo, contenido, imagen, fecha, created_at)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    'Entrenamientos de Básquet y Vóley',
                    'Se convoca a los estudiantes del equipo de Básquet y Vóley a los entrenamientos con los siguientes horarios.',
                    '../img/depo.png',
                    '2025-10-20',
                    datetime.utcnow().isoformat() + 'Z'
                ))
            elif table == 'horarios':
                conn.execute('''
                    INSERT INTO horarios (titulo, imagen, fecha, created_at)
                    VALUES (?, ?, ?, ?)
                ''', (
                    'Horario General de Clases',
                    '../img/horario_general.png',
                    '2025-01-01',
                    datetime.utcnow().isoformat() + 'Z'
                ))
                # Insertar un segundo horario de ejemplo
                conn.execute('''
                    INSERT INTO horarios (titulo, imagen, fecha, created_at)
                    VALUES (?, ?, ?, ?)
                ''', (
                    'Horario Lunes a Jueves',
                    '../img/horario_lun_jue.png',
                    '2025-01-01',
                    datetime.utcnow().isoformat() + 'Z'
                ))
                # Insertar un tercer horario de ejemplo
                conn.execute('''
                    INSERT INTO horarios (titulo, imagen, fecha, created_at)
                    VALUES (?, ?, ?, ?)
                ''', (
                    'Horario Viernes',
                    '../img/horario_viernes.png',
                    '2025-01-01',
                    datetime.utcnow().isoformat() + 'Z'
                ))
            elif table == 'profesores':
                # Dirección
                conn.execute('''
                    INSERT INTO profesores (nombre, cargo, area, especialidad, numero_celular, url_foto, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    'Director Silverio Aucachi',
                    'Director General',
                    'Dirección',
                    'Dirección General',
                    '(591) 7243-8903',
                    '',
                    datetime.utcnow().isoformat() + 'Z'
                ))
                
                # Comunicación y Lenguaje
                conn.execute('''
                    INSERT INTO profesores (nombre, cargo, area, especialidad, numero_celular, url_foto, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    'Prof. Fidelia Pinto',
                    'Docente',
                    'Comunicación y Lenguaje',
                    'Lengua Castellana y Literatura',
                    '(591) 7182-4559',
                    '',
                    datetime.utcnow().isoformat() + 'Z'
                ))
                
                conn.execute('''
                    INSERT INTO profesores (nombre, cargo, area, especialidad, numero_celular, url_foto, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    'Prof. Blanca',
                    'Docente',
                    'Comunicación y Lenguaje',
                    'Comunicación y Lenguaje',
                    '(591) 7386-2721',
                    '',
                    datetime.utcnow().isoformat() + 'Z'
                ))
                
                conn.execute('''
                    INSERT INTO profesores (nombre, cargo, area, especialidad, numero_celular, url_foto, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    'Prof. Tania',
                    'Docente',
                    'Comunicación y Lenguaje',
                    'Comunicación y Lenguaje',
                    '(591) 7242-1676',
                    '',
                    datetime.utcnow().isoformat() + 'Z'
                ))
                
                conn.execute('''
                    INSERT INTO profesores (nombre, cargo, area, especialidad, numero_celular, url_foto, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    'Prof. Primitiva',
                    'Docente',
                    'Comunicación y Lenguaje',
                    'Comunicación y Lenguaje',
                    '(591) 7238-7911',
                    '',
                    datetime.utcnow().isoformat() + 'Z'
                ))
                
                # Ciencias Sociales
                conn.execute('''
                    INSERT INTO profesores (nombre, cargo, area, especialidad, numero_celular, url_foto, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    'Prof. Sonia Pinto',
                    'Docente',
                    'Ciencias Sociales',
                    'Ciencias Sociales',
                    '(591) 6046-0289',
                    '',
                    datetime.utcnow().isoformat() + 'Z'
                ))
                
                conn.execute('''
                    INSERT INTO profesores (nombre, cargo, area, especialidad, numero_celular, url_foto, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    'Prof. Victor Hugo Alizares',
                    'Docente',
                    'Ciencias Sociales',
                    'Ciencias Sociales',
                    '(591) 7237-8017',
                    '',
                    datetime.utcnow().isoformat() + 'Z'
                ))
                
                conn.execute('''
                    INSERT INTO profesores (nombre, cargo, area, especialidad, numero_celular, url_foto, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    'Prof. Paola',
                    'Docente',
                    'Ciencias Sociales',
                    'Ciencias Sociales',
                    '(591) 7388-5099',
                    '',
                    datetime.utcnow().isoformat() + 'Z'
                ))
                
                conn.execute('''
                    INSERT INTO profesores (nombre, cargo, area, especialidad, numero_celular, url_foto, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    'Prof. Ramiro',
                    'Docente',
                    'Ciencias Sociales',
                    'Ciencias Sociales',
                    '(591) 6839-0904',
                    '',
                    datetime.utcnow().isoformat() + 'Z'
                ))
                
                conn.execute('''
                    INSERT INTO profesores (nombre, cargo, area, especialidad, numero_celular, url_foto, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    'Prof. Amanda',
                    'Docente',
                    'Ciencias Sociales',
                    'Ciencias Sociales',
                    '(591) 6839-0904',
                    '',
                    datetime.utcnow().isoformat() + 'Z'
                ))
                
                # Matemáticas
                conn.execute('''
                    INSERT INTO profesores (nombre, cargo, area, especialidad, numero_celular, url_foto, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    'Prof. Silvia',
                    'Docente',
                    'Matemáticas',
                    'Matemáticas',
                    '(591) 7238-9130',
                    '',
                    datetime.utcnow().isoformat() + 'Z'
                ))
                
                conn.execute('''
                    INSERT INTO profesores (nombre, cargo, area, especialidad, numero_celular, url_foto, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    'Prof. Deysi Porco',
                    'Docente',
                    'Matemáticas',
                    'Matemáticas',
                    '(591) 7388-2135',
                    '',
                    datetime.utcnow().isoformat() + 'Z'
                ))
                
                conn.execute('''
                    INSERT INTO profesores (nombre, cargo, area, especialidad, numero_celular, url_foto, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    'Prof. Elena',
                    'Docente',
                    'Matemáticas',
                    'Matemáticas',
                    '(591) 7425-1155',
                    '',
                    datetime.utcnow().isoformat() + 'Z'
                ))
                
                conn.execute('''
                    INSERT INTO profesores (nombre, cargo, area, especialidad, numero_celular, url_foto, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    'Prof. Carlos Mendieta',
                    'Docente',
                    'Matemáticas',
                    'Matemáticas',
                    '(591) 7240-8980',
                    '',
                    datetime.utcnow().isoformat() + 'Z'
                ))
                
                # Biología y Ciencias Naturales
                conn.execute('''
                    INSERT INTO profesores (nombre, cargo, area, especialidad, numero_celular, url_foto, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    'Prof. Norma',
                    'Docente',
                    'Biología y Ciencias Naturales',
                    'Biología',
                    '(591) 6791-8787',
                    '',
                    datetime.utcnow().isoformat() + 'Z'
                ))
                
                conn.execute('''
                    INSERT INTO profesores (nombre, cargo, area, especialidad, numero_celular, url_foto, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    'Prof. Benito Uño',
                    'Docente',
                    'Biología y Ciencias Naturales',
                    'Biología',
                    '(591) 7385-8231',
                    '',
                    datetime.utcnow().isoformat() + 'Z'
                ))
                
                # Lengua Extranjera (Inglés)
                conn.execute('''
                    INSERT INTO profesores (nombre, cargo, area, especialidad, numero_celular, url_foto, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    'Prof. Inés',
                    'Docente',
                    'Lengua Extranjera',
                    'Lengua Extranjera (Inglés)',
                    '(591) 6840-8389',
                    '',
                    datetime.utcnow().isoformat() + 'Z'
                ))
                
                conn.execute('''
                    INSERT INTO profesores (nombre, cargo, area, especialidad, numero_celular, url_foto, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    'Prof. Celia',
                    'Docente',
                    'Lengua Extranjera',
                    'Lengua Extranjera (Inglés)',
                    '(591) 7242-6349',
                    '',
                    datetime.utcnow().isoformat() + 'Z'
                ))
                
                conn.execute('''
                    INSERT INTO profesores (nombre, cargo, area, especialidad, numero_celular, url_foto, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    'Prof. Cristina Vaca',
                    'Docente',
                    'Lengua Extranjera',
                    'Lengua Extranjera (Inglés)',
                    '(591) 7243-1818',
                    '',
                    datetime.utcnow().isoformat() + 'Z'
                ))
                
                # Psicología y Filosofía
                conn.execute('''
                    INSERT INTO profesores (nombre, cargo, area, especialidad, numero_celular, url_foto, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    'Prof. Ana Liz',
                    'Docente',
                    'Psicología y Filosofía',
                    'Psicología',
                    '(591) 6841-5872',
                    '',
                    datetime.utcnow().isoformat() + 'Z'
                ))
                
                conn.execute('''
                    INSERT INTO profesores (nombre, cargo, area, especialidad, numero_celular, url_foto, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    'Prof. Helmer',
                    'Docente',
                    'Psicología y Filosofía',
                    'Psicología',
                    '(591) 7617-6260',
                    '',
                    datetime.utcnow().isoformat() + 'Z'
                ))
                
                conn.execute('''
                    INSERT INTO profesores (nombre, cargo, area, especialidad, numero_celular, url_foto, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    'Prof. Virgilia Cruz',
                    'Docente',
                    'Psicología y Filosofía',
                    'Filosofía',
                    '(591) 7285-2250',
                    '',
                    datetime.utcnow().isoformat() + 'Z'
                ))
                
                # Música
                conn.execute('''
                    INSERT INTO profesores (nombre, cargo, area, especialidad, numero_celular, url_foto, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    'Prof. Oscar',
                    'Docente',
                    'Técnica',
                    'Música',
                    '(591) 7240-1831',
                    '',
                    datetime.utcnow().isoformat() + 'Z'
                ))
                
                conn.execute('''
                    INSERT INTO profesores (nombre, cargo, area, especialidad, numero_celular, url_foto, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    'Prof. Milton Nina',
                    'Docente',
                    'Técnica',
                    'Música',
                    '(591) 7387-0246',
                    '',
                    datetime.utcnow().isoformat() + 'Z'
                ))

            elif table == 'usuarios':
                contrasena = hash_password('admin123')
                # Insertar usuarios de ejemplo
                
                conn.execute('''
                    INSERT INTO usuarios (username, nombre, password, created_at)
                    VALUES (?, ?, ?, ?)
                ''', (
                    'admin',
                    'Administrador del Sistema',
                    contrasena,
                    datetime.utcnow().isoformat() + 'Z'
                ))
                contrasena = hash_password('anita123')
                conn.execute('''
                    INSERT INTO usuarios (username, nombre, password, created_at)
                    VALUES (?, ?, ?, ?)
                ''', (
                    'anais',
                    'Anais Marca Salazar',
                    contrasena,
                    datetime.utcnow().isoformat() + 'Z'
                ))
    
    conn.commit()
    conn.close()

# Inicializar DB al arrancar
init_db()

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de health check actualizado"""
    return jsonify({
        'status': 'ok',
        'message': 'API funcionando correctamente',
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'endpoints': {
            'comunicados': '/api/comunicados',
            'blog': '/api/blog',
            'comentarios': '/api/comentarios',
            'deportes': '/api/deportes',
            'horarios': '/api/horarios',
            'usuarios': '/api/usuarios',
            'profesores': '/api/profesores'  # Agregar este
        }
    }), 200

@app.route('/', methods=['GET'])
def home():
    """Página de inicio de la API actualizada"""
    return jsonify({
        'message': 'Bienvenido a la API de José María Linares',
        'version': '2.0',
        'endpoints': {
            'health': '/health',
            'comunicados': '/api/comunicados',
            'blog': '/api/blog',
            'comentarios': '/api/comentarios',
            'deportes': '/api/deportes',
            'horarios': '/api/horarios',
            'usuarios': '/api/usuarios',
            'profesores': '/api/profesores'  # Agregar este
        }
    }), 200

# ==================== PROFESORES ====================

@app.route('/api/profesores', methods=['GET'])
def get_profesores():
    """Obtiene todos los profesores ordenados por área y nombre"""
    try:
        conn = get_db_connection()
        profesores = conn.execute(
            'SELECT * FROM profesores ORDER BY area, nombre'
        ).fetchall()
        conn.close()
        
        return jsonify([dict(p) for p in profesores]), 200
    except Exception as e:
        return jsonify({'error': 'Error al obtener profesores', 'details': str(e)}), 500

@app.route('/api/profesores', methods=['POST'])
def create_profesor():
    """Crea un nuevo profesor"""
    try:
        data = request.get_json()
        
        # Validaciones
        if not data:
            return jsonify({'error': 'No se enviaron datos'}), 400
        
        if not data.get('nombre'):
            return jsonify({'error': 'El campo "nombre" es obligatorio'}), 400
        
        if not data.get('cargo'):
            return jsonify({'error': 'El campo "cargo" es obligatorio'}), 400
        
        if not data.get('area'):
            return jsonify({'error': 'El campo "area" es obligatorio'}), 400
        
        if not data.get('especialidad'):
            return jsonify({'error': 'El campo "especialidad" es obligatorio'}), 400
        
        if not data.get('numero_celular'):
            return jsonify({'error': 'El campo "numero_celular" es obligatorio'}), 400
        
        # Crear profesor
        conn = get_db_connection()
        cursor = conn.execute(
            '''INSERT INTO profesores (nombre, cargo, area, especialidad, numero_celular, url_foto, created_at) 
               VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (
                data['nombre'],
                data['cargo'],
                data['area'],
                data['especialidad'],
                data['numero_celular'],
                data.get('url_foto', ''),
                datetime.utcnow().isoformat() + 'Z'
            )
        )
        conn.commit()
        profesor_id = cursor.lastrowid
        
        # Obtener el profesor creado
        profesor = conn.execute(
            'SELECT * FROM profesores WHERE id = ?', (profesor_id,)
        ).fetchone()
        conn.close()
        
        return jsonify(dict(profesor)), 201
    except Exception as e:
        return jsonify({'error': 'Error al crear profesor', 'details': str(e)}), 500

@app.route('/api/profesores/<int:id>', methods=['PUT'])
def update_profesor(id):
    """Actualiza un profesor existente"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No se enviaron datos'}), 400
        
        conn = get_db_connection()
        
        # Verificar que el profesor existe
        profesor = conn.execute('SELECT * FROM profesores WHERE id = ?', (id,)).fetchone()
        if not profesor:
            conn.close()
            return jsonify({'error': 'Profesor no encontrado'}), 404
        
        # Preparar campos a actualizar
        nombre = data.get('nombre', profesor['nombre'])
        cargo = data.get('cargo', profesor['cargo'])
        area = data.get('area', profesor['area'])
        especialidad = data.get('especialidad', profesor['especialidad'])
        numero_celular = data.get('numero_celular', profesor['numero_celular'])
        url_foto = data.get('url_foto', profesor['url_foto'])
        
        # Actualizar profesor
        conn.execute(
            '''UPDATE profesores 
               SET nombre = ?, cargo = ?, area = ?, especialidad = ?, numero_celular = ?, url_foto = ?
               WHERE id = ?''',
            (nombre, cargo, area, especialidad, numero_celular, url_foto, id)
        )
        conn.commit()
        
        # Obtener el profesor actualizado
        profesor_actualizado = conn.execute(
            'SELECT * FROM profesores WHERE id = ?', (id,)
        ).fetchone()
        conn.close()
        
        return jsonify(dict(profesor_actualizado)), 200
    except Exception as e:
        return jsonify({'error': 'Error al actualizar profesor', 'details': str(e)}), 500

@app.route('/api/profesores/<int:id>', methods=['DELETE'])
def delete_profesor(id):
    """Elimina un profesor"""
    try:
        conn = get_db_connection()
        
        # Verificar que el profesor existe
        profesor = conn.execute('SELECT * FROM profesores WHERE id = ?', (id,)).fetchone()
        if not profesor:
            conn.close()
            return jsonify({'error': 'Profesor no encontrado'}), 404
        
        # Eliminar profesor
        conn.execute('DELETE FROM profesores WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Profesor eliminado exitosamente'}), 200
    except Exception as e:
        return jsonify({'error': 'Error al eliminar profesor', 'details': str(e)}), 500

@app.route('/api/profesores/<int:id>', methods=['GET'])
def get_profesor(id):
    """Obtiene un profesor específico por ID"""
    try:
        conn = get_db_connection()
        profesor = conn.execute(
            'SELECT * FROM profesores WHERE id = ?', (id,)
        ).fetchone()
        conn.close()
        
        if not profesor:
            return jsonify({'error': 'Profesor no encontrado'}), 404
        
        return jsonify(dict(profesor)), 200
    except Exception as e:
        return jsonify({'error': 'Error al obtener profesor', 'details': str(e)}), 500

# ==================== USUARIOS ====================

@app.route('/api/usuarios', methods=['GET'])
def get_usuarios():
    """Obtiene todos los usuarios"""
    try:
        conn = get_db_connection()
        usuarios = conn.execute(
            'SELECT id, username, nombre, created_at FROM usuarios ORDER BY created_at DESC'
        ).fetchall()
        conn.close()
        
        return jsonify([dict(u) for u in usuarios]), 200
    except Exception as e:
        return jsonify({'error': 'Error al obtener usuarios', 'details': str(e)}), 500

@app.route('/api/usuarios', methods=['POST'])
def create_usuario():
    """Crea un nuevo usuario"""
    try:
        data = request.get_json()
        
        # Validaciones
        if not data:
            return jsonify({'error': 'No se enviaron datos'}), 400
        
        if not data.get('username'):
            return jsonify({'error': 'El campo "username" es obligatorio'}), 400
        
        if not data.get('nombre'):
            return jsonify({'error': 'El campo "nombre" es obligatorio'}), 400
        
        if not data.get('password'):
            return jsonify({'error': 'El campo "password" es obligatorio'}), 400
        
        # Verificar si el usuario ya existe
        conn = get_db_connection()
        usuario_existente = conn.execute(
            'SELECT id FROM usuarios WHERE username = ?', (data['username'],)
        ).fetchone()
        
        if usuario_existente:
            conn.close()
            return jsonify({'error': 'El nombre de usuario ya existe'}), 400
        
        # Crear usuario
        cursor = conn.execute(
            '''INSERT INTO usuarios (username, nombre, password, created_at) 
               VALUES (?, ?, ?, ?)''',
            (
                data['username'],
                data['nombre'],
                hash_password(data['password']),
                datetime.utcnow().isoformat() + 'Z'
            )
        )
        conn.commit()
        usuario_id = cursor.lastrowid
        
        # Obtener el usuario creado (sin password)
        usuario = conn.execute(
            'SELECT id, username, nombre, created_at FROM usuarios WHERE id = ?', (usuario_id,)
        ).fetchone()
        conn.close()
        
        return jsonify(dict(usuario)), 201
    except Exception as e:
        return jsonify({'error': 'Error al crear usuario', 'details': str(e)}), 500

@app.route('/api/usuarios/<int:id>', methods=['PUT'])
def update_usuario(id):
    """Actualiza un usuario existente"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No se enviaron datos'}), 400
        
        conn = get_db_connection()
        
        # Verificar que el usuario existe
        usuario = conn.execute('SELECT * FROM usuarios WHERE id = ?', (id,)).fetchone()
        if not usuario:
            conn.close()
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        # Verificar si el nuevo username ya existe (si se está cambiando)
        if 'username' in data and data['username'] != usuario['username']:
            usuario_existente = conn.execute(
                'SELECT id FROM usuarios WHERE username = ? AND id != ?', 
                (data['username'], id)
            ).fetchone()
            
            if usuario_existente:
                conn.close()
                return jsonify({'error': 'El nombre de usuario ya existe'}), 400
        
        # Preparar campos a actualizar
        username = data.get('username', usuario['username'])
        nombre = data.get('nombre', usuario['nombre'])
        
        # Actualizar contraseña solo si se proporciona
        if 'password' in data and data['password']:
            password = hash_password(data['password'])
        else:
            password = usuario['password']
        
        # Actualizar usuario
        conn.execute(
            '''UPDATE usuarios 
               SET username = ?, nombre = ?, password = ?
               WHERE id = ?''',
            (username, nombre, password, id)
        )
        conn.commit()
        
        # Obtener el usuario actualizado (sin password)
        usuario_actualizado = conn.execute(
            'SELECT id, username, nombre, created_at FROM usuarios WHERE id = ?', (id,)
        ).fetchone()
        conn.close()
        
        return jsonify(dict(usuario_actualizado)), 200
    except Exception as e:
        return jsonify({'error': 'Error al actualizar usuario', 'details': str(e)}), 500

@app.route('/api/usuarios/<int:id>', methods=['DELETE'])
def delete_usuario(id):
    """Elimina un usuario"""
    try:
        conn = get_db_connection()
        
        # Verificar que el usuario existe
        usuario = conn.execute('SELECT * FROM usuarios WHERE id = ?', (id,)).fetchone()
        if not usuario:
            conn.close()
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        # Eliminar usuario
        conn.execute('DELETE FROM usuarios WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Usuario eliminado exitosamente'}), 200
    except Exception as e:
        return jsonify({'error': 'Error al eliminar usuario', 'details': str(e)}), 500

@app.route('/api/usuarios/<int:id>', methods=['GET'])
def get_usuario(id):
    """Obtiene un usuario específico por ID"""
    try:
        conn = get_db_connection()
        usuario = conn.execute(
            'SELECT id, username, nombre, created_at FROM usuarios WHERE id = ?', (id,)
        ).fetchone()
        conn.close()
        
        if not usuario:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        return jsonify(dict(usuario)), 200
    except Exception as e:
        return jsonify({'error': 'Error al obtener usuario', 'details': str(e)}), 500


@app.route('/api/login', methods=['POST'])
def login():
    """Endpoint para autenticación de usuarios"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'message': 'No se enviaron datos'}), 400
        
        if not data.get('username'):
            return jsonify({'success': False, 'message': 'El campo "username" es obligatorio'}), 400
        
        if not data.get('password'):
            return jsonify({'success': False, 'message': 'El campo "password" es obligatorio'}), 400
        
        conn = get_db_connection()
        
        # Buscar usuario por username
        user = conn.execute(
            'SELECT * FROM usuarios WHERE username = ?', (data['username'],)
        ).fetchone()
        
        if not user:
            conn.close()
            return jsonify({'success': False, 'message': 'Usuario no encontrado'}), 401
        
        # Verificar contraseña (comparar hash)
        hashed_password = hash_password(data['password'])
        if user['password'] != hashed_password:
            conn.close()
            return jsonify({'success': False, 'message': 'Contraseña incorrecta'}), 401
        
        conn.close()
        
        # Login exitoso
        return jsonify({
            'success': True,
            'message': 'Login exitoso',
            'user': {
                'id': user['id'],
                'username': user['username'],
                'nombre': user['nombre']
            }
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': 'Error en el servidor', 'details': str(e)}), 500


# ==================== HORARIOS ====================

@app.route('/api/horarios', methods=['GET'])
def get_horarios():
    """Obtiene todos los horarios ordenados por fecha descendente"""
    try:
        conn = get_db_connection()
        horarios = conn.execute(
            'SELECT * FROM horarios ORDER BY fecha DESC, created_at DESC'
        ).fetchall()
        conn.close()
        
        return jsonify([dict(h) for h in horarios]), 200
    except Exception as e:
        return jsonify({'error': 'Error al obtener horarios', 'details': str(e)}), 500

@app.route('/api/horarios', methods=['POST'])
def create_horario():
    """Crea un nuevo horario"""
    try:
        data = request.get_json()
        
        # Validaciones
        if not data:
            return jsonify({'error': 'No se enviaron datos'}), 400
        
        if not data.get('titulo'):
            return jsonify({'error': 'El campo "titulo" es obligatorio'}), 400
        
        if not data.get('fecha'):
            return jsonify({'error': 'El campo "fecha" es obligatorio'}), 400
        
        # Validar formato de fecha
        try:
            datetime.fromisoformat(data['fecha'].replace('Z', '+00:00'))
        except ValueError:
            # Intentar formato YYYY-MM-DD
            try:
                datetime.strptime(data['fecha'], '%Y-%m-%d')
            except ValueError:
                return jsonify({'error': 'El campo "fecha" debe estar en formato YYYY-MM-DD o ISO8601'}), 400
        
        # Crear horario
        conn = get_db_connection()
        cursor = conn.execute(
            '''INSERT INTO horarios (titulo, imagen, fecha, created_at) 
               VALUES (?, ?, ?, ?)''',
            (
                data['titulo'],
                data.get('imagen', ''),
                data['fecha'],
                datetime.utcnow().isoformat() + 'Z'
            )
        )
        conn.commit()
        horario_id = cursor.lastrowid
        
        # Obtener el horario creado
        horario = conn.execute(
            'SELECT * FROM horarios WHERE id = ?', (horario_id,)
        ).fetchone()
        conn.close()
        
        return jsonify(dict(horario)), 201
    except Exception as e:
        return jsonify({'error': 'Error al crear horario', 'details': str(e)}), 500

@app.route('/api/horarios/<int:id>', methods=['PUT'])
def update_horario(id):
    """Actualiza un horario existente"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No se enviaron datos'}), 400
        
        conn = get_db_connection()
        
        # Verificar que el horario existe
        horario = conn.execute('SELECT * FROM horarios WHERE id = ?', (id,)).fetchone()
        if not horario:
            conn.close()
            return jsonify({'error': 'Horario no encontrado'}), 404
        
        # Preparar campos a actualizar (horarios no tiene campo 'contenido')
        titulo = data.get('titulo', horario['titulo'])
        imagen = data.get('imagen', horario['imagen'])
        fecha = data.get('fecha', horario['fecha'])
        
        # Validar fecha si se proporciona
        if 'fecha' in data:
            try:
                datetime.fromisoformat(fecha.replace('Z', '+00:00'))
            except ValueError:
                try:
                    datetime.strptime(fecha, '%Y-%m-%d')
                except ValueError:
                    conn.close()
                    return jsonify({'error': 'El campo "fecha" debe estar en formato YYYY-MM-DD o ISO8601'}), 400
        
        # Actualizar horario
        conn.execute(
            '''UPDATE horarios 
               SET titulo = ?, imagen = ?, fecha = ?
               WHERE id = ?''',
            (titulo, imagen, fecha, id)
        )
        conn.commit()
        
        # Obtener el horario actualizado
        horario_actualizado = conn.execute(
            'SELECT * FROM horarios WHERE id = ?', (id,)
        ).fetchone()
        conn.close()
        
        return jsonify(dict(horario_actualizado)), 200
    except Exception as e:
        return jsonify({'error': 'Error al actualizar horario', 'details': str(e)}), 500

@app.route('/api/horarios/<int:id>', methods=['DELETE'])
def delete_horario(id):
    """Elimina un horario"""
    try:
        conn = get_db_connection()
        
        # Verificar que el horario existe
        horario = conn.execute('SELECT * FROM horarios WHERE id = ?', (id,)).fetchone()
        if not horario:
            conn.close()
            return jsonify({'error': 'Horario no encontrado'}), 404
        
        # Eliminar horario
        conn.execute('DELETE FROM horarios WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Horario eliminado exitosamente'}), 200
    except Exception as e:
        return jsonify({'error': 'Error al eliminar horario', 'details': str(e)}), 500
# ==================== COMUNICADOS ====================

@app.route('/api/comunicados', methods=['GET'])
def get_comunicados():
    """Obtiene todos los comunicados ordenados por fecha descendente"""
    try:
        conn = get_db_connection()
        comunicados = conn.execute(
            'SELECT * FROM comunicados ORDER BY fecha DESC, created_at DESC'
        ).fetchall()
        conn.close()
        
        return jsonify([dict(c) for c in comunicados]), 200
    except Exception as e:
        return jsonify({'error': 'Error al obtener comunicados', 'details': str(e)}), 500

@app.route('/api/comunicados', methods=['POST'])
def create_comunicado():
    """Crea un nuevo comunicado"""
    try:
        data = request.get_json()
        
        # Validaciones
        if not data:
            return jsonify({'error': 'No se enviaron datos'}), 400
        
        if not data.get('titulo'):
            return jsonify({'error': 'El campo "titulo" es obligatorio'}), 400
        
        if not data.get('contenido'):
            return jsonify({'error': 'El campo "contenido" es obligatorio'}), 400
        
        if not data.get('fecha'):
            return jsonify({'error': 'El campo "fecha" es obligatorio'}), 400
        
        # Validar formato de fecha (más flexible)
        try:
            datetime.fromisoformat(data['fecha'].replace('Z', '+00:00'))
        except ValueError:
            # Intentar formato YYYY-MM-DD
            try:
                datetime.strptime(data['fecha'], '%Y-%m-%d')
            except ValueError:
                return jsonify({'error': 'El campo "fecha" debe estar en formato YYYY-MM-DD o ISO8601'}), 400
        
        # Crear comunicado
        conn = get_db_connection()
        cursor = conn.execute(
            '''INSERT INTO comunicados (titulo, contenido, imagen, fecha, created_at) 
               VALUES (?, ?, ?, ?, ?)''',
            (
                data['titulo'],
                data['contenido'],
                data.get('imagen', ''),
                data['fecha'],
                datetime.utcnow().isoformat() + 'Z'
            )
        )
        conn.commit()
        comunicado_id = cursor.lastrowid
        
        # Obtener el comunicado creado
        comunicado = conn.execute(
            'SELECT * FROM comunicados WHERE id = ?', (comunicado_id,)
        ).fetchone()
        conn.close()
        
        return jsonify(dict(comunicado)), 201
    except Exception as e:
        return jsonify({'error': 'Error al crear comunicado', 'details': str(e)}), 500

@app.route('/api/comunicados/<int:id>', methods=['PUT'])
def update_comunicado(id):
    """Actualiza un comunicado existente"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No se enviaron datos'}), 400
        
        conn = get_db_connection()
        
        # Verificar que el comunicado existe
        comunicado = conn.execute('SELECT * FROM comunicados WHERE id = ?', (id,)).fetchone()
        if not comunicado:
            conn.close()
            return jsonify({'error': 'Comunicado no encontrado'}), 404
        
        # Preparar campos a actualizar
        titulo = data.get('titulo', comunicado['titulo'])
        contenido = data.get('contenido', comunicado['contenido'])
        imagen = data.get('imagen', comunicado['imagen'])
        fecha = data.get('fecha', comunicado['fecha'])
        
        # Validar fecha si se proporciona
        if 'fecha' in data:
            try:
                datetime.fromisoformat(fecha.replace('Z', '+00:00'))
            except ValueError:
                try:
                    datetime.strptime(fecha, '%Y-%m-%d')
                except ValueError:
                    conn.close()
                    return jsonify({'error': 'El campo "fecha" debe estar en formato YYYY-MM-DD o ISO8601'}), 400
        
        # Actualizar comunicado
        conn.execute(
            '''UPDATE comunicados 
               SET titulo = ?, contenido = ?, imagen = ?, fecha = ?
               WHERE id = ?''',
            (titulo, contenido, imagen, fecha, id)
        )
        conn.commit()
        
        # Obtener el comunicado actualizado
        comunicado_actualizado = conn.execute(
            'SELECT * FROM comunicados WHERE id = ?', (id,)
        ).fetchone()
        conn.close()
        
        return jsonify(dict(comunicado_actualizado)), 200
    except Exception as e:
        return jsonify({'error': 'Error al actualizar comunicado', 'details': str(e)}), 500

@app.route('/api/comunicados/<int:id>', methods=['DELETE'])
def delete_comunicado(id):
    """Elimina un comunicado"""
    try:
        conn = get_db_connection()
        
        # Verificar que el comunicado existe
        comunicado = conn.execute('SELECT * FROM comunicados WHERE id = ?', (id,)).fetchone()
        if not comunicado:
            conn.close()
            return jsonify({'error': 'Comunicado no encontrado'}), 404
        
        # Eliminar comunicado
        conn.execute('DELETE FROM comunicados WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Comunicado eliminado exitosamente'}), 200
    except Exception as e:
        return jsonify({'error': 'Error al eliminar comunicado', 'details': str(e)}), 500

# ==================== BLOG ====================

@app.route('/api/blog', methods=['GET'])
def get_blog():
    """Obtiene todas las entradas del blog"""
    try:
        conn = get_db_connection()
        blog = conn.execute(
            'SELECT * FROM blog ORDER BY fecha DESC, created_at DESC'
        ).fetchall()
        conn.close()
        
        return jsonify([dict(b) for b in blog]), 200
    except Exception as e:
        return jsonify({'error': 'Error al obtener blog', 'details': str(e)}), 500

@app.route('/api/blog', methods=['POST'])
def create_blog():
    """Crea una nueva entrada de blog"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No se enviaron datos'}), 400
        
        if not data.get('titulo'):
            return jsonify({'error': 'El campo "titulo" es obligatorio'}), 400
        
        if not data.get('contenido'):
            return jsonify({'error': 'El campo "contenido" es obligatorio'}), 400
        
        if not data.get('categoria'):
            return jsonify({'error': 'El campo "categoria" es obligatorio'}), 400
        
        if not data.get('fecha'):
            return jsonify({'error': 'El campo "fecha" es obligatorio'}), 400
        
        try:
            datetime.fromisoformat(data['fecha'].replace('Z', '+00:00'))
        except ValueError:
            try:
                datetime.strptime(data['fecha'], '%Y-%m-%d')
            except ValueError:
                return jsonify({'error': 'El campo "fecha" debe estar en formato YYYY-MM-DD o ISO8601'}), 400
        
        conn = get_db_connection()
        cursor = conn.execute(
            '''INSERT INTO blog (titulo, contenido, categoria, imagen, fecha, created_at) 
               VALUES (?, ?, ?, ?, ?, ?)''',
            (
                data['titulo'],
                data['contenido'],
                data.get('categoria', '0000'),
                data.get('imagen', ''),
                data['fecha'],
                datetime.utcnow().isoformat() + 'Z'
            )
        )
        conn.commit()
        blog_id = cursor.lastrowid
        
        blog = conn.execute(
            'SELECT * FROM blog WHERE id = ?', (blog_id,)
        ).fetchone()
        conn.close()
        
        return jsonify(dict(blog)), 201
    except Exception as e:
        return jsonify({'error': 'Error al crear entrada de blog', 'details': str(e)}), 500

@app.route('/api/blog/<int:id>', methods=['PUT'])
def update_blog(id):
    """Actualiza una entrada de blog"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No se enviaron datos'}), 400
        
        conn = get_db_connection()
        
        blog = conn.execute('SELECT * FROM blog WHERE id = ?', (id,)).fetchone()
        if not blog:
            conn.close()
            return jsonify({'error': 'Entrada de blog no encontrada'}), 404
        
        titulo = data.get('titulo', blog['titulo'])
        contenido = data.get('contenido', blog['contenido'])
        categoria = data.get('categoria', blog['categoria'])
        imagen = data.get('imagen', blog['imagen'])
        fecha = data.get('fecha', blog['fecha'])
        
        if 'fecha' in data:
            try:
                datetime.fromisoformat(fecha.replace('Z', '+00:00'))
            except ValueError:
                try:
                    datetime.strptime(fecha, '%Y-%m-%d')
                except ValueError:
                    conn.close()
                    return jsonify({'error': 'El campo "fecha" debe estar en formato YYYY-MM-DD o ISO8601'}), 400
        
        conn.execute(
            '''UPDATE blog 
               SET titulo = ?, contenido = ?, categoria = ?, imagen = ?, fecha = ?
               WHERE id = ?''',
            (titulo, contenido, categoria, imagen, fecha, id)
        )
        conn.commit()
        
        blog_actualizado = conn.execute(
            'SELECT * FROM blog WHERE id = ?', (id,)
        ).fetchone()
        conn.close()
        
        return jsonify(dict(blog_actualizado)), 200
    except Exception as e:
        return jsonify({'error': 'Error al actualizar blog', 'details': str(e)}), 500

@app.route('/api/blog/<int:id>', methods=['DELETE'])
def delete_blog(id):
    """Elimina una entrada de blog"""
    try:
        conn = get_db_connection()
        
        blog = conn.execute('SELECT * FROM blog WHERE id = ?', (id,)).fetchone()
        if not blog:
            conn.close()
            return jsonify({'error': 'Entrada de blog no encontrada'}), 404
        
        conn.execute('DELETE FROM blog WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Entrada de blog eliminada exitosamente'}), 200
    except Exception as e:
        return jsonify({'error': 'Error al eliminar blog', 'details': str(e)}), 500

# ==================== COMENTARIOS ====================

@app.route('/api/comentarios', methods=['GET'])
def get_comentarios():
    """Obtiene todos los comentarios"""
    try:
        conn = get_db_connection()
        comentarios = conn.execute(
            'SELECT * FROM comentarios ORDER BY fecha DESC, created_at DESC'
        ).fetchall()
        conn.close()
        
        return jsonify([dict(c) for c in comentarios]), 200
    except Exception as e:
        return jsonify({'error': 'Error al obtener comentarios', 'details': str(e)}), 500

@app.route('/api/comentarios', methods=['POST'])
def create_comentario():
    """Crea un nuevo comentario"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No se enviaron datos'}), 400
        
        if not data.get('titulo'):
            return jsonify({'error': 'El campo "titulo" es obligatorio'}), 400
        
        if not data.get('contenido'):
            return jsonify({'error': 'El campo "contenido" es obligatorio'}), 400
        
        if not data.get('fecha'):
            return jsonify({'error': 'El campo "fecha" es obligatorio'}), 400
        
        try:
            datetime.fromisoformat(data['fecha'].replace('Z', '+00:00'))
        except ValueError:
            try:
                datetime.strptime(data['fecha'], '%Y-%m-%d')
            except ValueError:
                return jsonify({'error': 'El campo "fecha" debe estar en formato YYYY-MM-DD o ISO8601'}), 400
        
        conn = get_db_connection()
        cursor = conn.execute(
            '''INSERT INTO comentarios (titulo, contenido, imagen, fecha, created_at) 
               VALUES (?, ?, ?, ?, ?)''',
            (
                data['titulo'],
                data['contenido'],
                data.get('imagen', ''),
                data['fecha'],
                datetime.utcnow().isoformat() + 'Z'
            )
        )
        conn.commit()
        comentario_id = cursor.lastrowid
        
        comentario = conn.execute(
            'SELECT * FROM comentarios WHERE id = ?', (comentario_id,)
        ).fetchone()
        conn.close()
        
        return jsonify(dict(comentario)), 201
    except Exception as e:
        return jsonify({'error': 'Error al crear comentario', 'details': str(e)}), 500

@app.route('/api/comentarios/<int:id>', methods=['PUT'])
def update_comentario(id):
    """Actualiza un comentario"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No se enviaron datos'}), 400
        
        conn = get_db_connection()
        
        comentario = conn.execute('SELECT * FROM comentarios WHERE id = ?', (id,)).fetchone()
        if not comentario:
            conn.close()
            return jsonify({'error': 'Comentario no encontrado'}), 404
        
        titulo = data.get('titulo', comentario['titulo'])
        contenido = data.get('contenido', comentario['contenido'])
        imagen = data.get('imagen', comentario['imagen'])
        fecha = data.get('fecha', comentario['fecha'])
        
        if 'fecha' in data:
            try:
                datetime.fromisoformat(fecha.replace('Z', '+00:00'))
            except ValueError:
                try:
                    datetime.strptime(fecha, '%Y-%m-%d')
                except ValueError:
                    conn.close()
                    return jsonify({'error': 'El campo "fecha" debe estar en formato YYYY-MM-DD o ISO8601'}), 400
        
        conn.execute(
            '''UPDATE comentarios 
               SET titulo = ?, contenido = ?, imagen = ?, fecha = ?
               WHERE id = ?''',
            (titulo, contenido, imagen, fecha, id)
        )
        conn.commit()
        
        comentario_actualizado = conn.execute(
            'SELECT * FROM comentarios WHERE id = ?', (id,)
        ).fetchone()
        conn.close()
        
        return jsonify(dict(comentario_actualizado)), 200
    except Exception as e:
        return jsonify({'error': 'Error al actualizar comentario', 'details': str(e)}), 500

@app.route('/api/comentarios/<int:id>', methods=['DELETE'])
def delete_comentario(id):
    """Elimina un comentario"""
    try:
        conn = get_db_connection()
        
        comentario = conn.execute('SELECT * FROM comentarios WHERE id = ?', (id,)).fetchone()
        if not comentario:
            conn.close()
            return jsonify({'error': 'Comentario no encontrado'}), 404
        
        conn.execute('DELETE FROM comentarios WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Comentario eliminado exitosamente'}), 200
    except Exception as e:
        return jsonify({'error': 'Error al eliminar comentario', 'details': str(e)}), 500

# ==================== DEPORTES ====================

@app.route('/api/deportes', methods=['GET'])
def get_deportes():
    """Obtiene todas las actividades deportivas"""
    try:
        conn = get_db_connection()
        deportes = conn.execute(
            'SELECT * FROM deportes ORDER BY fecha DESC, created_at DESC'
        ).fetchall()
        conn.close()
        
        return jsonify([dict(d) for d in deportes]), 200
    except Exception as e:
        return jsonify({'error': 'Error al obtener deportes', 'details': str(e)}), 500

@app.route('/api/deportes', methods=['POST'])
def create_deporte():
    """Crea una nueva actividad deportiva"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No se enviaron datos'}), 400
        
        if not data.get('titulo'):
            return jsonify({'error': 'El campo "titulo" es obligatorio'}), 400
        
        if not data.get('contenido'):
            return jsonify({'error': 'El campo "contenido" es obligatorio'}), 400
        
        if not data.get('fecha'):
            return jsonify({'error': 'El campo "fecha" es obligatorio'}), 400
        
        try:
            datetime.fromisoformat(data['fecha'].replace('Z', '+00:00'))
        except ValueError:
            try:
                datetime.strptime(data['fecha'], '%Y-%m-%d')
            except ValueError:
                return jsonify({'error': 'El campo "fecha" debe estar en formato YYYY-MM-DD o ISO8601'}), 400
        
        conn = get_db_connection()
        cursor = conn.execute(
            '''INSERT INTO deportes (titulo, contenido, imagen, fecha, created_at) 
               VALUES (?, ?, ?, ?, ?)''',
            (
                data['titulo'],
                data['contenido'],
                data.get('imagen', ''),
                data['fecha'],
                datetime.utcnow().isoformat() + 'Z'
            )
        )
        conn.commit()
        deporte_id = cursor.lastrowid
        
        deporte = conn.execute(
            'SELECT * FROM deportes WHERE id = ?', (deporte_id,)
        ).fetchone()
        conn.close()
        
        return jsonify(dict(deporte)), 201
    except Exception as e:
        return jsonify({'error': 'Error al crear actividad deportiva', 'details': str(e)}), 500

@app.route('/api/deportes/<int:id>', methods=['PUT'])
def update_deporte(id):
    """Actualiza una actividad deportiva"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No se enviaron datos'}), 400
        
        conn = get_db_connection()
        
        deporte = conn.execute('SELECT * FROM deportes WHERE id = ?', (id,)).fetchone()
        if not deporte:
            conn.close()
            return jsonify({'error': 'Actividad deportiva no encontrada'}), 404
        
        titulo = data.get('titulo', deporte['titulo'])
        contenido = data.get('contenido', deporte['contenido'])
        imagen = data.get('imagen', deporte['imagen'])
        fecha = data.get('fecha', deporte['fecha'])
        
        if 'fecha' in data:
            try:
                datetime.fromisoformat(fecha.replace('Z', '+00:00'))
            except ValueError:
                try:
                    datetime.strptime(fecha, '%Y-%m-%d')
                except ValueError:
                    conn.close()
                    return jsonify({'error': 'El campo "fecha" debe estar en formato YYYY-MM-DD o ISO8601'}), 400
        
        conn.execute(
            '''UPDATE deportes 
               SET titulo = ?, contenido = ?, imagen = ?, fecha = ?
               WHERE id = ?''',
            (titulo, contenido, imagen, fecha, id)
        )
        conn.commit()
        
        deporte_actualizado = conn.execute(
            'SELECT * FROM deportes WHERE id = ?', (id,)
        ).fetchone()
        conn.close()
        
        return jsonify(dict(deporte_actualizado)), 200
    except Exception as e:
        return jsonify({'error': 'Error al actualizar actividad deportiva', 'details': str(e)}), 500

@app.route('/api/deportes/<int:id>', methods=['DELETE'])
def delete_deporte(id):
    """Elimina una actividad deportiva"""
    try:
        conn = get_db_connection()
        
        deporte = conn.execute('SELECT * FROM deportes WHERE id = ?', (id,)).fetchone()
        if not deporte:
            conn.close()
            return jsonify({'error': 'Actividad deportiva no encontrada'}), 404
        
        conn.execute('DELETE FROM deportes WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Actividad deportiva eliminada exitosamente'}), 200
    except Exception as e:
        return jsonify({'error': 'Error al eliminar actividad deportiva', 'details': str(e)}), 500

# ==================== MANEJO DE ERRORES ====================

@app.errorhandler(404)
def not_found(error):
    """Manejo de rutas no encontradas"""
    return jsonify({'error': 'Ruta no encontrada'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Manejo de errores internos del servidor"""
    return jsonify({'error': 'Error interno del servidor'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)