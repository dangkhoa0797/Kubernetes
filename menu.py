#!/usr/bin/python3
import time
import os
import subprocess
from simple_term_menu import TerminalMenu

# main menu
def main():
    main_menu_title = "  Main Menu.\n  Press Q or Esc to quit. \n"
    main_menu_items = ["[1] Install ansible", "[2] Edit hosts file", "[3] Edit variables file", "[4] Deploy Kubernetes", "Quit"]
    main_menu_cursor = ">> "
    main_menu_cursor_style = ("fg_blue", "bold")
    main_menu_style = ("bg_red", "fg_yellow")
    main_menu_exit = False

    main_menu = TerminalMenu(
        menu_entries=main_menu_items,
        title=main_menu_title,
        menu_cursor=main_menu_cursor,
        menu_cursor_style=main_menu_cursor_style,
        menu_highlight_style=main_menu_style,
        cycle_cursor=True,
        clear_screen=False,
    )
# submenu
    deploy_kubernetes_title = "  Install cluster.\n  Press Q or Esc to back to main menu. \n"
    deploy_kubernetes_items = ["[1] Deploy kubernester cluster *", "[2] Infratructure service", "[3] Deploy Traefik", "[4] Base service", "Back to Main Menu"]
    deploy_kubernetes_back = False
    deploy_kubernetes = TerminalMenu(
        deploy_kubernetes_items,
        title=deploy_kubernetes_title,
        menu_cursor=main_menu_cursor,
        menu_cursor_style=main_menu_cursor_style,
        menu_highlight_style=main_menu_style,
        cycle_cursor=True,
        clear_screen=False,
    )
# main menu seletor    
    while not main_menu_exit:
        main_sel = main_menu.show()

        if main_sel == 0:
            print("install ansible")
            os.system("apt install python3-pip -y; pip3 install ansible; mkdir -p /etc/ansible/")
            subprocess.run('ssh-keygen -b 2048 -t rsa -f /root/.ssh/id_rsa -q -N "" 0>&-', shell=True)
        if main_sel == 1:
            print("Cập nhật file hosts")
            time.sleep(1)
            subprocess.run("nano hosts; cp -f ./hosts /etc/ansible/hosts", shell=True)
            print("Copy keygen ssh: write Yes and import Password")
            time.sleep(2)
            os.system("grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}' hosts > server.txt")
            os.system("chmod a+x kubernetes/copykeygen.sh; kubernetes/copykeygen.sh")           
        elif main_sel == 2:
            print("Cập nhật file variables.yml")
            subprocess.run("nano kubernetes/variables.yml", shell=True)
            time.sleep(3)
# submenu seletor 
        elif main_sel == 3:
            while not deploy_kubernetes_back:
                edit_sel = deploy_kubernetes.show()
                if edit_sel == 0:
                    print("Deploy kubernester cluster *")
                    subprocess.run("ansible-playbook kubernetes/dependent-components.yaml; ansible-playbook kubernetes/master.yaml; ansible-playbook kubernetes/worker.yaml; ansible-playbook kubernetes/replace.yaml; ansible-playbook kubernetes/nfs-StorageClass/setupnfs.yaml; ansible-playbook kubernetes/metallb/setupmetallb.yaml; ansible-playbook kubernetes/infra/setupportainer.yaml", shell=True)
                    time.sleep(3)
                elif edit_sel == 1:
                    print("Infratructure service")
                    subprocess.run("ansible-playbook kubernetes/infra/setupinfra.yaml", shell=True)
                    time.sleep(3)
                elif edit_sel == 2:
                    print("Deploy Traefik")
                    subprocess.run("ansible-playbook kubernetes/replace.yaml --tags traefik; ansible-playbook kubernetes/traefik/setup.yaml", shell=True)
                    time.sleep(3)
                elif edit_sel == 3:
                    print("Base service")
                    subprocess.run("ansible-playbook kubernetes/replace.yaml --tags basesvc; ansible-playbook kubernetes/basesvc/setupbasesvc.yaml", shell=True)
                    time.sleep(3)
                elif edit_sel == 4 or edit_sel == None:
                    deploy_kubernetes_back = True
                    print("Back Selected")
            deploy_kubernetes_back = False

        elif main_sel == 4 or main_sel == None:
            main_menu_exit = True
            print("Quit Selected")


if __name__ == "__main__":
    main()
