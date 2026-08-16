from home_aggregate import (
    CountResults,
    HomeReport,
    TruncatedResults,
)


class ResponseFormatter:
    _DEVICE_LABELS = {
        "window": {
            "singular": "finestra",
            "plural": "finestre",
        },
        "door": {
            "singular": "porta",
            "plural": "porte",
        },
        "light": {
            "singular": "entit\u00e0 light",
            "plural": "entit\u00e0 light",
        },
        "switch": {
            "singular": "switch",
            "plural": "switch",
        },
        "automation": {
            "singular": "automazione",
            "plural": "automazioni",
        },
    }

    _STATE_LABELS = {
        "window": {
            "on": "aperte",
            "off": "chiuse",
        },
        "door": {
            "on": "aperte",
            "off": "chiuse",
        },
        "light": {
            "on": "accese",
            "off": "spente",
        },
    }

    @classmethod
    def format_home_state_results(
        cls,
        results,
        device_kind=None,
        desired_state=None,
    ):
        state_label = None

        if device_kind and desired_state:
            labels = cls._STATE_LABELS.get(device_kind)

            if labels:
                state_label = labels.get(desired_state)

        return cls._format_entity_results(
            results,
            state_label,
        )

    @classmethod
    def format_truncated_state_results(
        cls,
        truncated: TruncatedResults,
        device_kind=None,
        desired_state=None,
    ):
        state_label = None

        if device_kind and desired_state:
            labels = cls._STATE_LABELS.get(device_kind)

            if labels:
                state_label = labels.get(desired_state)

        names = [
            item["name"]
            for item in truncated.items
        ]

        if not names:
            return "Non risultano entit\u00e0 corrispondenti alla richiesta."

        formatted_names = cls._format_name_list(names)

        if truncated.remaining_count > 0:
            formatted_names = (
                formatted_names
                + " e altre "
                + str(truncated.remaining_count)
                + " entit\u00e0"
            )

        if state_label:
            return (
                "Risultano "
                + state_label
                + ": "
                + formatted_names
                + "."
            )

        return formatted_names + "."

    @classmethod
    def format_count_results(
        cls,
        results: CountResults,
    ):
        ordered_targets = [
            "window",
            "door",
            "light",
            "switch",
            "automation",
        ]

        parts = []

        for target in ordered_targets:
            if target not in results.counts:
                continue

            count = results.counts[target]
            parts.append(
                str(count)
                + " "
                + cls._label_for_count(
                    target,
                    count,
                )
            )

        if not parts:
            return "Nessun conteggio disponibile."

        response = "Risultano " + cls._format_name_list(parts) + "."

        if "automation" in results.counts:
            response += (
                " Automazioni: "
                + str(results.automation_on)
                + " abilitate, "
                + str(results.automation_off)
                + " disabilitate, "
                + str(results.automation_unknown)
                + " unknown e "
                + str(results.automation_unavailable)
                + " unavailable."
            )

        return response

    @classmethod
    def format_home_report(
        cls,
        report: HomeReport,
    ):
        windows_text = cls._format_report_section(
            report.windows_open,
        )

        doors_text = cls._format_report_section(
            report.doors_open,
        )

        lights_text = cls._format_report_section(
            report.lights_on,
        )

        return " ".join([
            "Finestre aperte: " + windows_text + ".",
            "Porte aperte: " + doors_text + ".",
            "Entit\u00e0 light accese: " + lights_text + ".",
            (
                "Automazioni: "
                + str(report.automation_on)
                + " abilitate, "
                + str(report.automation_off)
                + " disabilitate, "
                + str(report.automation_unknown)
                + " unknown e "
                + str(report.automation_unavailable)
                + " unavailable."
            ),
            "Entit\u00e0 unavailable: " + str(report.unavailable_total) + ".",
        ])

    @staticmethod
    def _format_entity_results(results, state_label=None):
        if not results:
            return "Non risultano entit\u00e0 corrispondenti alla richiesta."

        names = [item["name"] for item in results]

        formatted_names = ResponseFormatter._format_name_list(names)

        if state_label:
            return f"Risultano {state_label}: {formatted_names}."

        return formatted_names + "."

    @classmethod
    def _label_for_count(
        cls,
        device_kind: str,
        count: int,
    ) -> str:
        labels = cls._DEVICE_LABELS.get(device_kind)

        if not labels:
            return device_kind

        if count == 1:
            return labels["singular"]

        return labels["plural"]

    @classmethod
    def _format_report_section(
        cls,
        section: TruncatedResults,
    ) -> str:
        if section.total_count == 0:
            return "nessuna"

        names = [
            item["name"]
            for item in section.items
        ]

        formatted_names = cls._format_name_list(names)

        if section.remaining_count > 0:
            return (
                formatted_names
                + " e altre "
                + str(section.remaining_count)
                + " entit\u00e0"
            )

        return formatted_names

    @staticmethod
    def _format_name_list(names: list[str]) -> str:
        if len(names) == 1:
            return names[0]

        return ", ".join(names[:-1]) + " e " + names[-1]




