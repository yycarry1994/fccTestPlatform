

class Validator(object):

    def __init__(self, context, resp_obj):
        self.context = context
        self.resp_obj = resp_obj

    def eval_check_item(self, validator, resp_obj):
        """ evaluate check item in validator
        @param (dict) validator
            {"check": "status_code", "comparator": "eq", "expect": 201}
            {"check": "$resp_body_success", "comparator": "eq", "expect": True}
        @param (object) resp_obj
        @return (dict) validator info
            {
                "check": "status_code",
                "check_value": 200,
                "expect": 201,
                "comparator": "eq"
            }
        """
        check_item = validator["check"]
        # check_item should only be the following 5 formats:
        # 1, variable reference, e.g. $token
        # 2, function reference, e.g. ${is_status_code_200($status_code)}
        # 3, dict or list, maybe containing variable/function reference, e.g. {"var": "$abc"}
        # 4, string joined by delimiter. e.g. "status_code", "headers.content-type"
        # 5, regex string, e.g. "LB[\d]*(.*)RB[\d]*"

        if isinstance(check_item, (dict, list)) \
            or testcase.extract_variables(check_item) \
            or testcase.extract_functions(check_item):
            # format 1/2/3
            check_value = self.eval_content(check_item)
        else:
            try:
                # format 4/5
                check_value = resp_obj.extract_field(check_item)
            except exception.ParseResponseError:
                msg = "failed to extract check item from response!\n"
                msg += "response content: {}".format(resp_obj.content)
                raise exception.ParseResponseError(msg)

        validator["check_value"] = check_value

        # expect_value should only be in 2 types:
        # 1, variable reference, e.g. $expect_status_code
        # 2, actual value, e.g. 200
        expect_value = self.eval_content(validator["expect"])
        validator["expect"] = expect_value
        return validator

    def do_validation(self, validator_dict):
        """ validate with functions
        """
        # TODO: move comparator uniform to init_test_suites
        comparator = utils.get_uniform_comparator(validator_dict["comparator"])
        validate_func = self.testcase_parser.get_bind_function(comparator)

        if not validate_func:
            raise exception.FunctionNotFound("comparator not found: {}".format(comparator))

        check_item = validator_dict["check"]
        check_value = validator_dict["check_value"]
        expect_value = validator_dict["expect"]

        if (check_value is None or expect_value is None) \
            and comparator not in ["is", "eq", "equals", "=="]:
            raise exception.ParamsError("Null value can only be compared with comparator: eq/equals/==")

        try:
            validate_func(validator_dict["check_value"], validator_dict["expect"])
        except (AssertionError, TypeError):
            err_msg = "\n" + "\n".join([
                "\tcheck item name: %s;" % check_item,
                "\tcheck item value: %s (%s);" % (check_value, type(check_value).__name__),
                "\tcomparator: %s;" % comparator,
                "\texpected value: %s (%s)." % (expect_value, type(expect_value).__name__)
            ])
            raise exception.ValidationError(err_msg)

    def validate(self, validators, resp_obj):
        """ check validators with the context variable mapping.
        @param (list) validators
        @param (object) resp_obj
        """
        for validator in validators:
            validator_dict = self.eval_check_item(
                testcase.parse_validator(validator),
                resp_obj
            )
            self.do_validation(validator_dict)

        return True
