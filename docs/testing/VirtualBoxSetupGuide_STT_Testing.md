# VirtualBox Setup Guide for STT Project Testing

This guide provides the recommended steps for setting up a stable and performant Ubuntu 24.04 virtual machine in VirtualBox. Following these instructions will create a consistent environment for testing the STT application and avoid common issues like installation slowness, system freezes, and missing clipboard functionality.

## Prerequisites

- VirtualBox installed on the host machine.
- An Ubuntu 24.04 Desktop ISO file downloaded.

## Reference Host Hardware

This configuration was tested and validated on the following host system. Performance may vary on other hardware, but the stability settings should apply universally.

- **Operating System:** Manjaro Linux
- **Kernel:** 6.6.94
- **Processor:** 16 × AMD Ryzen 7 3700X
- **Memory:** 31.3 GiB of RAM
- **Graphics Processor:** NVIDIA GeForce GTX 1050 Ti

---

## Part 1: VM Creation and Configuration

These settings are critical for performance and stability.

### Step 1.1: Create the New Virtual Machine

1.  In VirtualBox, click **New**.
2.  **Name:** `Ubuntu STT Tester` (or similar).
3.  **ISO Image:** Leave this field blank.
4.  Check the box: **"Skip Unattended Installation"**.
5.  Click **Next**.
6.  **Hardware:**
    -   **Base Memory:** `4096 MB` or more.
    -   **Processors:** `4` or more.
7.  Click **Next**.

### Step 1.2: Create the Virtual Hard Disk (CRITICAL)

This is the most important step for fast installation and performance.

1.  Select **"Create a Virtual Hard Disk Now"**.
2.  Set the disk size to **40 GB** or more.
3.  On the next screen, change the storage type to **"Fixed size"**.
    > **Why?** A fixed-size disk is pre-allocated and prevents the massive I/O bottleneck that occurs when a "Dynamically allocated" disk constantly resizes during installation.
4.  Click **Create** and wait for the process to finish.

### Step 1.3: Final VM Settings

Select the newly created VM and click **Settings**. Configure the following:

-   **System -> Motherboard:**
    -   **Chipset:** `ICH9`
    -   Check **"Enable EFI (special OSes only)"**.

-   **Display -> Screen:**
    -   **Graphics Controller:** `VMSVGA`
    -   **Uncheck "Enable 3D Acceleration"**.
    > **Why?** 3D acceleration is a common cause of system hangs and freezes in Linux guests. Disabling it significantly improves stability.

-   **Storage:**
    -   Select the **SATA Controller**. Check the box **"Use Host I/O Cache"**.
    -   Select the virtual disk file (`.vdi`). Check the box **"Solid-state Drive"**.
    -   Select the **Empty** optical drive. Click the CD icon on the right and **"Choose a disk file..."** to attach your Ubuntu 24.04 ISO.

Click **OK** to save all settings.

---

## Part 2: Ubuntu OS Installation

1.  Start the VM.
2.  Proceed through the language and keyboard setup.
3.  When you reach "Updates and other software", select:
    -   **Minimal installation**.
    -   **Uncheck** "Download updates while installing Ubuntu".
4.  Continue with the installation until it is complete.
5.  When finished, reboot the VM. At the prompt, remove the installation medium (press Enter).

---

## Part 3: Post-Installation (Guest Additions)

This step enables clipboard sharing, drag-and-drop, and automatic screen resizing.

### Step 3.1: Install Guest Additions ISO on Host (If Needed)

On your **host machine**, ensure the Guest Additions ISO package is installed.

-   **On Arch / Manjaro:**
    ```bash
    sudo pacman -S virtualbox-guest-iso
    ```
-   **On Debian / Ubuntu:**
    ```bash
    sudo apt install virtualbox-guest-additions-iso
    ```

### Step 3.2: Install Guest Additions Inside the Ubuntu VM

Perform these steps **inside your running Ubuntu VM**.

1.  **Prepare Ubuntu:** Open a terminal and run the following commands to install build dependencies.
    ```bash
    sudo apt update
    sudo apt install build-essential dkms linux-headers-$(uname -r)
    ```
2.  **Insert the CD:** From the VirtualBox top menu, go to **Devices -> Insert Guest Additions CD Image...**.
3.  **Run the Installer:**
    - A dialog may pop up asking to run the software. Click **Run**.
    - If no dialog appears, open the File Manager, right-click the `VBox_GAs...` CD, choose **"Open in Terminal"**, and run the command:
      ```bash
      sudo ./VBoxLinuxAdditions.run
      ```
4.  **Reboot:** After the installation completes, reboot the VM.
    ```bash
    reboot
    ```
5.  **Enable Features:** After rebooting, go to the **Devices** menu and enable **Shared Clipboard -> Bidirectional** and **Drag and Drop -> Bidirectional**.

Your stable, performant testing environment is now ready.

