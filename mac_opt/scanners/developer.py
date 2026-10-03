import os
import subprocess
import re
from typing import List
from mac_opt.models import CleanableItem, CleanableCategory, RiskLevel
from mac_opt.utils import get_path_size


def scan_developer_tools() -> List[CleanableItem]:
    """Scan developer tools, iOS simulators, Xcode, and Android build caches."""
    home = os.path.expanduser("~")
    items: List[CleanableItem] = []

    # 1. iOS Simulator Runtimes (Root /Library)
    try:
        res = subprocess.run(
            ["xcrun", "simctl", "runtime", "list"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if res.returncode == 0:
            lines = res.stdout.splitlines()
            current_platform = None
            for line in lines:
                line_str = line.strip()
                if line_str.startswith("--") and line_str.endswith("--"):
                    current_platform = line_str.replace("-", "").strip()
                elif "(" in line_str and ")" in line_str and "-" in line_str:
                    # e.g. iOS 18.6 (22G86) - 22A3A8D5-3860-4AD4-A83A-75805960250F (Ready)
                    match = re.search(r"^(.*?)\s+\((.*?)\)\s+-\s+([0-9A-Fa-f-]+)", line_str)
                    if match:
                        name = match.group(1).strip()
                        build = match.group(2).strip()
                        uuid = match.group(3).strip()
                        
                        # Root simulator volume size
                        runtime_dir = f"/Library/Developer/CoreSimulator/Volumes/{current_platform or 'iOS'}_{build}"
                        size = get_path_size(runtime_dir)
                        if size == 0:
                            # Also check root Cryptex / CoreSimulator size
                            size = get_path_size("/Library/Developer/CoreSimulator")

                        items.append(
                            CleanableItem(
                                id=f"sim_runtime_{uuid}",
                                title=f"iOS Simulator Runtime ({name})",
                                description=f"Installed disk image and mounted volume ({build}). Re-downloadable in Xcode.",
                                path=runtime_dir,
                                category=CleanableCategory.DEVELOPER,
                                risk=RiskLevel.REVIEW,
                                size_bytes=size,
                                selected=False,
                                custom_action="simctl_runtime",
                                details={"runtime_id": uuid, "name": name}
                            )
                        )
    except Exception:
        pass

    # 2. Simulator Devices Data (Per-user)
    sim_devices_path = os.path.join(home, "Library", "Developer", "CoreSimulator", "Devices")
    sim_devices_size = get_path_size(sim_devices_path)
    items.append(
        CleanableItem(
            id="sim_devices_erase",
            title="iOS Simulator Device Containers",
            description="Installed test apps, temp data, and caches in simulated iPhones/iPads",
            path=sim_devices_path,
            category=CleanableCategory.DEVELOPER,
            risk=RiskLevel.SAFE,
            size_bytes=sim_devices_size,
            selected=(sim_devices_size > 50 * 1024 * 1024),
            custom_action="simctl_erase"
        )
    )

    # 3. Xcode DerivedData
    derived_data_path = os.path.join(home, "Library", "Developer", "Xcode", "DerivedData")
    derived_size = get_path_size(derived_data_path)
    items.append(
        CleanableItem(
            id="xcode_derived_data",
            title="Xcode DerivedData (Build Artifacts)",
            description="Intermediate build outputs, modules, and indexing files. Safe to delete (Xcode will rebuild).",
            path=derived_data_path,
            category=CleanableCategory.DEVELOPER,
            risk=RiskLevel.SAFE,
            size_bytes=derived_size,
            selected=(derived_size > 100 * 1024 * 1024)
        )
    )

    # 4. Xcode iOS Device Logs
    device_logs_path = os.path.join(home, "Library", "Developer", "Xcode", "iOS Device Logs")
    logs_size = get_path_size(device_logs_path)
    items.append(
        CleanableItem(
            id="xcode_device_logs",
            title="Xcode iOS Device Crash Logs",
            description="Crash symbolication logs synced from connected physical devices",
            path=device_logs_path,
            category=CleanableCategory.DEVELOPER,
            risk=RiskLevel.SAFE,
            size_bytes=logs_size,
            selected=False
        )
    )

    # 5. Gradle Caches
    gradle_cache_path = os.path.join(home, ".gradle", "caches")
    gradle_size = get_path_size(gradle_cache_path)
    items.append(
        CleanableItem(
            id="gradle_caches",
            title="Android Gradle Build Cache",
            description="Downloaded dependencies, wrappers, and transform caches used by Android / Flutter builds",
            path=gradle_cache_path,
            category=CleanableCategory.DEVELOPER,
            risk=RiskLevel.SAFE,
            size_bytes=gradle_size,
            selected=False
        )
    )

    # 6. CocoaPods Cache
    cocoapods_cache_path = os.path.join(home, "Library", "Caches", "CocoaPods")
    if not os.path.exists(cocoapods_cache_path):
        cocoapods_cache_path = os.path.join(home, ".cocoapods")
    cocoapods_size = get_path_size(cocoapods_cache_path)
    items.append(
        CleanableItem(
            id="cocoapods_cache",
            title="CocoaPods Spec & Download Cache",
            description="Cached iOS pod repository git metadata and downloaded pods",
            path=cocoapods_cache_path,
            category=CleanableCategory.DEVELOPER,
            risk=RiskLevel.SAFE,
            size_bytes=cocoapods_size,
            selected=False
        )
    )

    return items
