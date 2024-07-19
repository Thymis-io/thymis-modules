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

    hostname = Setting(
        name="homeassistant.hostname",
        type="string",
        default="home-assistant.example.com",
        description="The hostname to reach Home Assistant as a virtual host in Nginx.",
        example="home-assistant.example.com",
    )

    port = Setting(
        name="homeassistant.port",
        type="string",
        default="8123",
        description="The port to reach Home Assistant.",
        example="8123",
    )

    exposePort = Setting(
        name="homeassistant.exposePort",
        type="bool",
        default="true",
        description="Expose the Home Assistant port to the network.",
        example="true",
    )


    def write_nix_settings(
        self, f, module_settings: thymis_controller.models.ModuleSettings, priority: int
    ):
        timezone = (
            module_settings.settings["timezone"]
            if "timezone" in module_settings.settings
            else self.timezone.default
        )

        hostname = (
            module_settings.settings["hostname"]
            if "hostname" in module_settings.settings
            else self.hostname.default
        )

        port = (
            module_settings.settings["port"]
            if "port" in module_settings.settings
            else self.port.default
        )

        exposePort = (
            module_settings.settings["exposePort"]
            if "exposePort" in module_settings.settings
            else self.exposePort.default
        )

        f.write(
            f"""
            services.home-assistant.enable = true;
            services.home-assistant.config.http.server_port = {port};
            services.home-assistant.config.homeassistant.time_zone = "{timezone}";
            services.nginx = {{
                enable = true;
                recommendedProxySettings = true;
                virtualHosts."{hostname}" = {{
                    extraConfig = ''
                        proxy_buffering off;
                    '';
                    locations."/" = {{
                        proxyPass = "http://[::1]:{port}";
                        proxyWebsockets = true;
                    }};
                }};
            }};
            """
        )
        if exposePort:
            f.write(
                f"""
                services.home-assistant.openFirewall = true;
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

class Nginx(Module):
    displayName: str = "Nginx"
    icon: str = thymis_controller.lib.read_into_base64(
        pathlib.Path(__file__).parent / "assets" / "nginx.svg"
    )

    def write_nix_settings(
        self, f, module_settings: thymis_controller.models.ModuleSettings, priority: int
    ):
        f.write(
            f"""
            services.nginx.enable = true;
            networking.firewall.allowedTCPPorts = [ 80 443 ];
            """
        )
