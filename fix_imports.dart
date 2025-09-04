#!/usr/bin/env dart

import 'dart:io';

Future<void> main() async {
  print('🔧 Import Path Fix Tool');
  print('======================\n');
  
  final projectDir = Directory('/hologram/data/project/turecarga');
  Directory.current = projectDir;
  
  final libDir = Directory('lib');
  if (!libDir.existsSync()) {
    print('❌ lib directory not found');
    return;
  }
  
  // Find all Dart files with import issues
  final dartFiles = await libDir
      .list(recursive: true)
      .where((entity) => entity.path.endsWith('.dart'))
      .cast<File>()
      .toList();
  
  print('📁 Scanning ${dartFiles.length} Dart files...\n');
  
  int filesWithIssues = 0;
  int totalImportIssues = 0;
  
  for (final file in dartFiles) {
    try {
      final content = await file.readAsString();
      final lines = content.split('\n');
      
      bool hasIssues = false;
      int issuesInFile = 0;
      
      for (int i = 0; i < lines.length; i++) {
        final line = lines[i];
        if (line.contains('package:cubalink23/')) {
          if (!hasIssues) {
            print('📄 Issues in: ${file.path.replaceAll('/hologram/data/project/turecarga/', '')}');
            hasIssues = true;
            filesWithIssues++;
          }
          print('   Line ${i + 1}: $line');
          issuesInFile++;
          totalImportIssues++;
        }
      }
      
      if (hasIssues) {
        print('   → $issuesInFile import issues found\n');
      }
      
    } catch (e) {
      print('❌ Error reading ${file.path}: $e');
    }
  }
  
  print('📊 SUMMARY');
  print('==================');
  print('Files scanned: ${dartFiles.length}');
  print('Files with import issues: $filesWithIssues');
  print('Total import issues: $totalImportIssues');
  
  if (totalImportIssues > 0) {
    print('\n🔧 TO FIX THESE ISSUES:');
    print('1. The package name in pubspec.yaml is: cubalink23');
    print('2. All imports using "package:cubalink23/" should use "package:cubalink23/"');
    print('3. Run this command to fix all at once:');
    print('   find lib -name "*.dart" -type f -exec sed -i "s/package:cubalink23\\//package:cubalink23\\//g" {} \\;');
    print('\nOR convert to relative imports for better maintainability.');
  } else {
    print('\n✅ No import issues found!');
  }
}