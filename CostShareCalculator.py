class HealthInsurancePlan:
    def __init__(self, copay, coinsurance_rate, copay_applies_oopmax, coins_applies_oopmax, deductible_applies_oopmax,
                 copay_continue_deductible_met, copay_continue_oopmax_met, copay_count_to_deductible,
                 is_deductible_before_copay, d_calculated, oopmax_calculated):
        self.copay = copay
        self.coinsurance_rate = coinsurance_rate
        self.copay_applies_oopmax = copay_applies_oopmax
        self.coins_applies_oopmax = coins_applies_oopmax
        self.deductible_applies_oopmax = deductible_applies_oopmax
        self.copay_continue_deductible_met = copay_continue_deductible_met
        self.copay_continue_oopmax_met = copay_continue_oopmax_met
        self.copay_count_to_deductible = copay_count_to_deductible
        self.is_deductible_before_copay = is_deductible_before_copay
        self.d_calculated = d_calculated
        self.oopmax_calculated = oopmax_calculated

    def calculate_patient_pay(self, service_cost, is_service_covered, benefit_limitation, deductible_code_exists,
                               cost_share_copay, cost_share_coinsurance, oopmax_i_calculated, oopmax_f_calculated,
                               di_calculated, df_calculated, limit_calculated_value, limit_type):
        self.copay = cost_share_copay
        self.coinsurance_rate = cost_share_coinsurance

        self.oopmax_calculated = min(oopmax_i_calculated if oopmax_i_calculated > 0 else oopmax_f_calculated,
                                     self.oopmax_calculated)
        self.d_calculated = min(di_calculated if di_calculated > 0 else df_calculated,
                                df_calculated if df_calculated > 0 else di_calculated)

        # Service not covered
        if not is_service_covered:
            print("Service not covered")
            return service_cost

        # OOPMAX limit met
        if self.oopmax_calculated == 0 and not self.copay_continue_oopmax_met:
            print("OOPMAX met")
            return 0.0

        # Deductible logic
        if self.is_deductible_before_copay:
            if self.d_calculated > 0 and deductible_code_exists:
                if service_cost <= self.d_calculated:
                    self.d_calculated -= service_cost
                    if self.deductible_applies_oopmax:
                        if service_cost <= self.oopmax_calculated:
                            self.oopmax_calculated -= service_cost
                        else:
                            member_cost = self.oopmax_calculated
                            self.oopmax_calculated = 0
                            return self.copay + member_cost
                    return service_cost
                else:
                    service_cost -= self.d_calculated
                    if self.deductible_applies_oopmax:
                        if self.d_calculated <= self.oopmax_calculated:
                            self.oopmax_calculated -= self.d_calculated
                        else:
                            self.oopmax_calculated = 0
                            return self.copay + service_cost
            elif self.d_calculated >= service_cost:
                self.d_calculated -= service_cost
                return self.copay + service_cost
            else:
                service_cost -= self.d_calculated
                member_cost = self.copay + service_cost
                if self.deductible_applies_oopmax:
                    if member_cost <= self.oopmax_calculated:
                        self.oopmax_calculated -= member_cost
                    else:
                        return self.oopmax_calculated
                return self.copay + self.d_calculated + self.calculate_coinsurance(service_cost, self.oopmax_calculated)

        # Deductible already met
        else:
            service_cost -= self.d_calculated
            if self.deductible_applies_oopmax:
                if self.d_calculated <= self.oopmax_calculated:
                    self.oopmax_calculated -= self.d_calculated
                else:
                    self.oopmax_calculated = 0
                    return self.copay + service_cost
            return self.copay + service_cost

        # Copay logic
        if self.copay > 0 and (self.oopmax_calculated > 0 or self.copay_continue_deductible_met):
            if self.copay <= service_cost:
                service_cost -= self.copay
                if self.copay_applies_oopmax:
                    if self.oopmax_calculated == service_cost and not self.is_deductible_before_copay:
                        self.d_calculated = service_cost
                        return service_cost
        return self.calculate_coinsurance(service_cost, self.oopmax_calculated)

    def calculate_coinsurance(self, service_cost, oopmax_calculated):
        coinsurance_amount = service_cost * self.coinsurance_rate
        if coinsurance_amount <= oopmax_calculated or not self.coins_applies_oopmax:
            self.oopmax_calculated -= coinsurance_amount
            return coinsurance_amount
        else:
            return oopmax_calculated


# Use case
plan = HealthInsurancePlan(
    copay=0.0,
    coinsurance_rate=0.0,
    copay_applies_oopmax=True,
    coins_applies_oopmax=False,
    deductible_applies_oopmax=False,
    copay_continue_deductible_met=False,
    copay_continue_oopmax_met=False,
    copay_count_to_deductible=False,
    is_deductible_before_copay=True,
    d_calculated=0.0,
    oopmax_calculated=0.0
)

service_cost = 161.0
is_service_covered = True
benefit_limitation = None
deductible_code_exists = False
cost_share_copay = 30.0
cost_share_coinsurance = 0.0
oopmax_i_calculated = 6000.0
oopmax_f_calculated = 12000.0
di_calculated = 0.0
df_calculated = 0.0
limit_calculated_value = 0
limit_type = "Dollar"

out_of_pocket_cost = plan.calculate_patient_pay(
    service_cost, is_service_covered, benefit_limitation, deductible_code_exists,
    cost_share_copay, cost_share_coinsurance, oopmax_i_calculated, oopmax_f_calculated,
    di_calculated, df_calculated, limit_calculated_value, limit_type
)

print(f"You Pay ${out_of_pocket_cost}")