# test_database.py - Tests pour database.py
import os
import sys
from datetime import datetime

# Importer les fonctions de database.py
import database

# Couleurs pour l'affichage
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"
BLUE = "\033[94m"

def print_test(test_name, passed):
    """Affiche le résultat d'un test"""
    if passed:
        print(f"{GREEN}✓{RESET} {test_name}")
    else:
        print(f"{RED}✗{RESET} {test_name}")
    return passed

def cleanup_test_db():
    """Supprime la base de données de test"""
    if os.path.exists("todos.db"):
        os.remove("todos.db")
        print(f"{BLUE}Base de données de test nettoyée{RESET}\n")

def test_1_init_db():
    """Test 1 : Initialisation de la base de données"""
    print(f"\n{BLUE}=== Test 1 : Initialisation de la base de données ==={RESET}")
    
    # Nettoyer avant de commencer
    cleanup_test_db()
    
    # Initialiser la BD
    database.init_db()
    
    # Vérifier que le fichier existe
    exists = os.path.exists("todos.db")
    print_test("Le fichier todos.db est créé", exists)
    
    # Vérifier que la table existe
    connexion = database.get_connexion()
    curseur = connexion.cursor()
    curseur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tasks'")
    table_exists = curseur.fetchone() is not None
    connexion.close()
    
    print_test("La table tasks existe", table_exists)
    
    return exists and table_exists

def test_2_add_task():
    """Test 2 : Ajouter des tâches"""
    print(f"\n{BLUE}=== Test 2 : Ajouter des tâches ==={RESET}")
    
    # Ajouter 3 tâches
    database.add_task("Apprendre Python")
    database.add_task("Créer une API")
    database.add_task("Tester le code")
    
    # Vérifier qu'elles sont bien ajoutées
    tasks = database.get_all_tasks()
    
    test_count = print_test("3 tâches ajoutées", len(tasks) == 3)
    test_first = print_test("Première tâche correcte", tasks[0]["title"] == "Apprendre Python")
    test_completed = print_test("Tâche non complétée par défaut", tasks[0]["completed"] == False)
    test_has_date = print_test("Date de création présente", "created_at" in tasks[0])
    
    print(f"\n{BLUE}Tâches créées :{RESET}")
    for task in tasks:
        status = "✓" if task["completed"] else "○"
        print(f"  {status} [{task['id']}] {task['title']} (créée le {task['created_at']})")
    
    return test_count and test_first and test_completed and test_has_date

def test_3_get_all_tasks():
    """Test 3 : Récupérer toutes les tâches"""
    print(f"\n{BLUE}=== Test 3 : Récupérer toutes les tâches ==={RESET}")
    
    tasks = database.get_all_tasks()
    
    test_list = print_test("Retourne une liste", isinstance(tasks, list))
    test_dict = print_test("Chaque élément est un dictionnaire", isinstance(tasks[0], dict))
    test_keys = print_test("Contient les bonnes clés", 
                          all(key in tasks[0] for key in ["id", "title", "completed", "created_at"]))
    test_bool = print_test("'completed' est un booléen", isinstance(tasks[0]["completed"], bool))
    
    return test_list and test_dict and test_keys and test_bool

def test_4_update_task():
    """Test 4 : Mettre à jour une tâche"""
    print(f"\n{BLUE}=== Test 4 : Mettre à jour une tâche ==={RESET}")
    
    # Récupérer la première tâche
    tasks = database.get_all_tasks()
    first_task_id = tasks[0]["id"]
    
    # Marquer comme complétée
    database.update_task(first_task_id, True)
    
    # Vérifier
    tasks = database.get_all_tasks()
    task_completed = tasks[0]["completed"]
    
    test_complete = print_test("Tâche marquée comme complétée", task_completed == True)
    
    # Marquer comme non complétée
    database.update_task(first_task_id, False)
    tasks = database.get_all_tasks()
    task_not_completed = tasks[0]["completed"]
    
    test_uncomplete = print_test("Tâche marquée comme non complétée", task_not_completed == False)
    
    print(f"\n{BLUE}Statut après mise à jour :{RESET}")
    for task in tasks:
        status = "✓" if task["completed"] else "○"
        print(f"  {status} [{task['id']}] {task['title']}")
    
    return test_complete and test_uncomplete

def test_5_delete_task():
    """Test 5 : Supprimer une tâche"""
    print(f"\n{BLUE}=== Test 5 : Supprimer une tâche ==={RESET}")
    
    # Récupérer le nombre initial
    tasks_before = database.get_all_tasks()
    count_before = len(tasks_before)
    task_to_delete_id = tasks_before[0]["id"]
    
    # Supprimer la première tâche
    database.delete_task(task_to_delete_id)
    
    # Vérifier
    tasks_after = database.get_all_tasks()
    count_after = len(tasks_after)
    
    test_count = print_test(f"Nombre de tâches : {count_before} → {count_after}", count_after == count_before - 1)
    test_deleted = print_test("Tâche bien supprimée", not any(t["id"] == task_to_delete_id for t in tasks_after))
    
    print(f"\n{BLUE}Tâches restantes :{RESET}")
    for task in tasks_after:
        status = "✓" if task["completed"] else "○"
        print(f"  {status} [{task['id']}] {task['title']}")
    
    return test_count and test_deleted

def test_6_integration():
    """Test 6 : Test d'intégration complet"""
    print(f"\n{BLUE}=== Test 6 : Scénario complet ==={RESET}")
    
    # Nettoyer et recommencer
    cleanup_test_db()
    database.init_db()
    
    # Ajouter plusieurs tâches
    database.add_task("Faire les courses")
    database.add_task("Lire un livre")
    database.add_task("Faire du sport")
    database.add_task("Appeler un ami")
    
    # Marquer certaines comme complétées
    tasks = database.get_all_tasks()
    database.update_task(tasks[0]["id"], True)
    database.update_task(tasks[2]["id"], True)
    
    # Supprimer une tâche
    database.delete_task(tasks[1]["id"])
    
    # Vérifications finales
    final_tasks = database.get_all_tasks()
    
    test_count = print_test("3 tâches restantes", len(final_tasks) == 3)
    test_completed = print_test("2 tâches complétées", sum(1 for t in final_tasks if t["completed"]) == 2)
    test_not_completed = print_test("1 tâche non complétée", sum(1 for t in final_tasks if not t["completed"]) == 1)
    
    print(f"\n{BLUE}État final :{RESET}")
    for task in final_tasks:
        status = "✓" if task["completed"] else "○"
        print(f"  {status} [{task['id']}] {task['title']}")
    
    return test_count and test_completed and test_not_completed

def run_all_tests():
    """Exécute tous les tests"""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}  TESTS DE LA BASE DE DONNÉES TODO LIST{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")
    
    results = []
    
    # Exécuter tous les tests
    results.append(("Initialisation DB", test_1_init_db()))
    results.append(("Ajouter tâches", test_2_add_task()))
    results.append(("Récupérer tâches", test_3_get_all_tasks()))
    results.append(("Mettre à jour tâche", test_4_update_task()))
    results.append(("Supprimer tâche", test_5_delete_task()))
    results.append(("Test d'intégration", test_6_integration()))
    
    # Résumé
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}  RÉSUMÉ DES TESTS{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        print_test(test_name, result)
    
    print(f"\n{BLUE}Résultat : {passed}/{total} tests réussis{RESET}")
    
    if passed == total:
        print(f"\n{GREEN}🎉 Tous les tests sont passés ! Bravo !{RESET}\n")
    else:
        print(f"\n{RED}❌ Certains tests ont échoué. Vérifie ton code.{RESET}\n")
    
    # Nettoyer après les tests
    cleanup_test_db()
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
