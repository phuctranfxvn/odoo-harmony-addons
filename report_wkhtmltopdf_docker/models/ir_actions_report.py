import os
import subprocess
import tempfile
from markupsafe import Markup
from odoo import models, _
from odoo.addons.base.models import ir_actions_report


# Set default path for temporary files
DEFAULT_TEMP_DIR = "/tmp/docker-report-odoo-temp"
os.makedirs(DEFAULT_TEMP_DIR, exist_ok=True)
tempfile.tempdir = DEFAULT_TEMP_DIR

# Custom _get_wkhtmltopdf_bin function
def _get_wkhtmltopdf_docker_bin():
    return [
        "docker",
        "run",
        "--rm",
        "-v",
        f"{DEFAULT_TEMP_DIR}:{DEFAULT_TEMP_DIR}",
        "madnight/docker-alpine-wkhtmltopdf",
    ]

# Custom POpen function
original_popen = subprocess.Popen
def custom_popen(command, *args, **kwargs):
    if isinstance(command[0], list):
        command = command[0] + command[1:]
    return original_popen(command, *args, **kwargs)


# Patch the original functions
ir_actions_report.tempfile = tempfile
ir_actions_report.subprocess.Popen = custom_popen
ir_actions_report._get_wkhtmltopdf_bin = _get_wkhtmltopdf_docker_bin


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    def _run_wkhtmltopdf(
        self,
        bodies,
        report_ref=False,
        header=None,
        footer=None,
        landscape=False,
        specific_paperformat_args=None,
        set_viewport_size=False,
    ):

        report_url = self.env['ir.config_parameter'].sudo().get_param('report.url')
        if not report_url:
            report_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        
        host_url = "http://host.docker.internal:8069"
        # Update the HTML files
        bodies = [
            Markup(str(body).replace(report_url, host_url))
            for body in bodies
        ]
        header = (
            Markup(str(header).replace(report_url, host_url))
            if header
            else None
        )
        footer = (
            Markup(str(footer).replace(report_url, host_url))
            if footer
            else None
        )

        return super(IrActionsReport, self)._run_wkhtmltopdf(
            bodies,
            report_ref=report_ref,
            header=header,
            footer=footer,
            landscape=landscape,
            specific_paperformat_args=specific_paperformat_args,
            set_viewport_size=set_viewport_size,
        )
