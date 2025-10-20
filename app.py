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
    """Inicializa la base de datos con la tabla comunicados"""
    conn = get_db_connection()
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
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }), 200

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
        
        # Validar formato de fecha
        try:
            datetime.fromisoformat(data['fecha'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'El campo "fecha" debe estar en formato ISO8601'}), 400
        
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
                conn.close()
                return jsonify({'error': 'El campo "fecha" debe estar en formato ISO8601'}), 400
        
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