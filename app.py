from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas las rutas

DATABASE = 'comunicados.db'

def get_db_connection():
    """Establece conexión con la base de datos SQLite"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

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
    
    # Insertar datos de ejemplo si las tablas están vacías
    for table in ['comunicados', 'blog', 'comentarios', 'deportes']:
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
            elif table == 'blog':
                conn.execute('''
                    INSERT INTO blog (titulo, contenido, imagen, fecha, created_at)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    '¡Campeones del Torneo!',
                    'Resumen de la emocionante final de fútbol sala.',
                    'Deportes',
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
    
    conn.commit()
    conn.close()

# Inicializar DB al arrancar
init_db()

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de health check"""
    return jsonify({
        'status': 'ok',
        'message': 'API funcionando correctamente',
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'endpoints': {
            'comunicados': '/api/comunicados',
            'blog': '/api/blog',
            'comentarios': '/api/comentarios',
            'deportes': '/api/deportes'
        }
    }), 200

@app.route('/', methods=['GET'])
def home():
    """Página de inicio de la API"""
    return jsonify({
        'message': 'Bienvenido a la API de José María Linares',
        'version': '1.0',
        'endpoints': {
            'health': '/health',
            'comunicados': '/api/comunicados',
            'blog': '/api/blog',
            'comentarios': '/api/comentarios',
            'deportes': '/api/deportes'
        }
    }), 200

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
            '''INSERT INTO blog (titulo, contenido, imagen, fecha, created_at) 
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
               SET titulo = ?, contenido = ?, imagen = ?, fecha = ?
               WHERE id = ?''',
            (titulo, contenido, imagen, fecha, id)
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