import thymis_controller
import thymis_controller.lib
import pathlib

from thymis_controller.models import Setting, ModuleSettings
from thymis_controller.modules import Module


class HomeAssistant(Module):
    displayName: str = "Home Assistant"
    icon: str = thymis_controller.lib.read_into_base64(
        pathlib.Path(__file__).parent / "assets" / "home-assistant.png"
    )


    timezone = Setting(
        name="homeassistant.timezone",
        type="string",
        default="Europe/Berlin",
        description="The timezone for Home Assistant.",
        example="Europe/Berlin",
    )

    def write_nix_settings(
        self, f, module_settings: thymis_controller.models.ModuleSettings, priority: int
    ):
        timezone = (
            module_settings.settings["timezone"]
            if "timezone" in module_settings.settings
            else self.timezone.default
        )
        f.write(
            f"""
            services.home-assistant.enable = true;
            services.home-assistant.openFirewall = true;
            services.home-assistant.config.homeassistant.time_zone = "{timezone}";
            """
        )

class HomeAssistant(Module):
    displayName: str = "Home Assistant"
    icon: str = thymis_controller.lib.read_into_base64(
        pathlib.Path(__file__).parent / "assets" / "home-assistant.png"
    )


    timezone = Setting(
        name="homeassistant.timezone",
        type="string",
        default="Europe/Berlin",
        description="The timezone for Home Assistant.",
        example="Europe/Berlin",
    )

    def write_nix_settings(
        self, f, module_settings: thymis_controller.models.ModuleSettings, priority: int
    ):
        timezone = (
            module_settings.settings["timezone"]
            if "timezone" in module_settings.settings
            else self.timezone.default
        )
        f.write(
            f"""
            services.home-assistant.enable = true;
            services.home-assistant.openFirewall = true;
            services.home-assistant.config.homeassistant.time_zone = "{timezone}";
            """
        )


class ESPHome(Module):
    displayName: str = "ESPHome"
    icon: str = thymis_controller.lib.read_into_base64(
        pathlib.Path(__file__).parent / "assets" / "esphome.svg"
    )

    def write_nix_settings(
        self, f, module_settings: thymis_controller.models.ModuleSettings, priority: int
    ):
        f.write(
            f"""
            services.esphome.enable = true;
            services.esphome.openFirewall = true;
            """
        )

class NodeRED(Module):
    displayName: str = "Node-RED"
    icon: str = thymis_controller.lib.read_into_base64(
        pathlib.Path(__file__).parent / "assets" / "node-red.svg"
    )

    def write_nix_settings(
        self, f, module_settings: thymis_controller.models.ModuleSettings, priority: int
    ):
        f.write(
            f"""
            services.node-red.enable = true;
            services.node-red.openFirewall = true;
            """
        )
