import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';

class SqliteService {
  static Database? _database;

  Future<Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDatabase();
    return _database!;
  }

  Future<Database> _initDatabase() async {
    final path = join(await getDatabasesPath(), 'gurukul_ai.db');
    return await openDatabase(
      path,
      version: 2,
      onCreate: (db, version) async {
        await _createTables(db);
      },
      onUpgrade: (db, oldVersion, newVersion) async {
        if (oldVersion < 2) {
          await db.execute('''
            CREATE TABLE embeddings (
              node_id TEXT PRIMARY KEY,
              vector BLOB,
              metadata TEXT
            )
          ''');
        }
      },
    );
  }

  Future<void> _createTables(Database db) async {
    // Search index table with FTS5
    await db.execute('''
      CREATE VIRTUAL TABLE search_index USING fts5(
        node_id UNINDEXED,
        title,
        subject,
        class_level,
        content,
        keywords
      )
    ''');

    // Processing queue table
    await db.execute('''
      CREATE TABLE processing_queue (
        id TEXT PRIMARY KEY,
        file_path TEXT,
        status TEXT,
        progress REAL,
        stage TEXT,
        checksum TEXT,
        updated_at TEXT
      )
    ''');

    // Semantic embeddings table
    await db.execute('''
      CREATE TABLE embeddings (
        node_id TEXT PRIMARY KEY,
        vector BLOB,
        metadata TEXT
      )
    ''');
  }
}
