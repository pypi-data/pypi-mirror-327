import json


def print_formatted(raw_output):
    print(json.dumps(raw_output, default=str))


def parse_execution_args(args):
    if args.get("input_config"):
        args["input_config"] = json.loads(args["input_config"])
    if args.get("output_config"):
        args["output_config"] = json.loads(args["output_config"])
    if args.get("tags"):
        args["tags"] = json.loads(args["tags"])
    if args.get("filter_by_tags"):
        args["filter_by_tags"] = json.loads(args["filter_by_tags"])
    if args.get("compute"):
        args["compute"] = json.loads(args["compute"])
    if args.get("termination_condition"):
        args["termination_condition"] = json.loads(args["termination_condition"])

    none_args = {key: value for (key, value) in args.items() if value is not None}

    return none_args
