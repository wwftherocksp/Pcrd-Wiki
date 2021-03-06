
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import TemplateView, View, ListView, DetailView
from django.shortcuts import get_list_or_404, get_object_or_404
from itertools import zip_longest
from django.http import HttpResponseNotFound
from django.urls import reverse
# Create your views here.
from pcrd_unpack import models
from collections import OrderedDict
from pcrd_unpack.utils import skill_utility

class EquipmentView(TemplateView):
    """docstring for """
    template_name = "pcrd_unpack/equipment.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        eq = get_object_or_404(models.EquipmentData, pk=self.kwargs["equipment_id"])
        context['equipment'] = eq
        drops = eq.questrewarddatacustom_set.all().order_by('quest__area_id')
        quests = [i.quest for i in drops]
        quests.sort(key=lambda x: x.area_id)
        # before python3.6 dict do not keep order, use OrderedDict
        context['drop_info'] = OrderedDict(zip(quests, [q.questrewarddatacustom_set.order_by('-rate') for q in quests]))
        if eq.craft_flg:
            cinfo = get_object_or_404(models.EquipmentCraft, pk=self.kwargs["equipment_id"])
            context["craft_info"] = cinfo
            components = {}
            for i in range(1, 11):
                eqid = getattr(cinfo, "condition_equipment_id_{}".format(i))
                eq_num = getattr(cinfo, "consume_num_{}".format(i))
                if eqid:
                    components[eqid] = eq_num
            context["components"] = components
        return context


class EquipmentListView(ListView):
    """docstring for Equi"""
    template_name = "pcrd_unpack/equipment_list.html"

    # model = models.EquipmentData

    def get_queryset(self):
        return models.EquipmentData.objects.order_by("-promotion_level")


class ItemView(TemplateView):
    """docstring for """
    template_name = "pcrd_unpack/item.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = get_object_or_404(models.ItemData, pk=self.kwargs["item_id"])
        context['item'] = item
        drops = item.questrewarddatacustom_set.all().order_by('quest__area_id')
        quests = [i.quest for i in drops]
        context['drop_info'] = OrderedDict(zip(quests, [q.questrewarddatacustom_set.order_by('-rate') for q in quests]))
        return context


# class ItemListView(ListView):
#     """docstring for Equi"""
#     template_name = "pcrd_unpack/item_list.html"
#     # model = models.EquipmentData
#
#     def get_queryset(self):
#         return models.ItemData.objects.order_by("-promotion_level")


class QuestAreaListView(ListView):
    """docstring for QuestAreaListView"""
    template_name = "pcrd_unpack/quests_list.html"
    model = models.QuestAreaData


class QuestAreaDetailView(TemplateView):
    """docstring for QuestAreaDetailView"""
    template_name = "pcrd_unpack/quest_area_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        area_id = self.kwargs["area_id"]
        area = get_object_or_404(models.QuestAreaData.objects, pk=area_id)
        context["area_title"] = area.area_name
        quests_in_charpter = models.QuestData.objects.filter(area_id=area_id)
        context["quests_in_charpter"] = quests_in_charpter
        context["quest_reward"] = {}
        for q in quests_in_charpter:
            context["quest_reward"][q] = q.questrewarddatacustom_set.order_by('-rate')
        return context


class UnitListView(ListView):
    """docstring for UnitListView"""
    template_name = "pcrd_unpack/unit_list.html"
    model = models.UnitData

    def get_queryset(self, **hints):
        return self.model.available_unit().order_by("-rarity")


class UnitDetailView(TemplateView):
    """docstring for UnitDetailView"""
    template_name = "pcrd_unpack/unit_detail/unit_detail.html"
    skill_type_table = {

    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        unit_id = kwargs["unit_id"]
        unit_data = get_object_or_404(models.UnitData, pk=unit_id)
        unit_data.comment = unit_data.comment.replace("\\n", "\n")
        unit_profile = get_object_or_404(models.UnitProfile, pk=unit_id)
        unit_promotion = get_list_or_404(models.UnitPromotion, pk=unit_id)
        unit_skill = get_object_or_404(models.UnitSkillData, pk=unit_id)
        skills = [
            get_object_or_404(models.SkillData, skill_id=getattr(unit_skill, f.name))
            for f in type(unit_skill)._meta.get_fields()
            if (not f.primary_key and getattr(unit_skill, f.name) != 0)
        ]
        unit_skills = {skill: self.get_skill_actions(skill) for skill in skills}
        context["unit_data"] = unit_data
        context["unit_profile"] = unit_profile
        context["unit_promotion"] = unit_promotion
        context["unit_skills"] = unit_skills
        ur = models.UnitSummary
        # properties = [
        #     ur.hp, ur.hp_recovery_rate, ur.wave_hp_recovery,
        #     ur.energy_recovery_rate, ur.wave_energy_recovery,
        #     ur.atk, ur.magic_str,
        #     ur.def_field, ur.magic_def,
        #     ur.physical_critical, ur.magic_critical,
        #     ur.dodge,
        #     ur.life_steal,
        # ]
        context["data_tags"] = ur.data_tags()
        # make 1d data tags to
        # 1 2 3
        # 4 5 6
        # 7
        context["table_data_tags"] = zip_longest(*[iter(context["data_tags"])] * 3, fillvalue=None)
        unit_pattern = get_object_or_404(models.UnitAttackPattern, unit_id=unit_id)
        # patterns = [
        #     getattr(unit_pattern, f.name)
        #     for f in type(unit_skill)._meta.get_fields()
        #     if (not f.primary_key and f.name.startswith("atk_pattern_"))
        # ]
        patterns = []
        for i in range(unit_pattern.loop_end):
            p = getattr(unit_pattern, 'atk_pattern_{}'.format(i+1))
            if p not in [0, 1]:
                # skill_pattern = int(unit_pattern.unit_id / 100) * 1000 + p - 1000 + 1
                # p = get_object_or_404(models.SkillData, skill_id=skill_pattern).name
                p = "Skill {}".format(p-1000)
            patterns.append(p)

        context['unit_patterns'] = {
            'loop_start': unit_pattern.loop_start,
            'patterns': patterns,
        }
        add_max_info(context)
        return context

    def get_skill_actions(self, skill: models.SkillData):
        actions = [get_object_or_404(models.SkillAction, action_id=getattr(skill, f.name))
                   for f in type(skill)._meta.get_fields()
                   if not f.primary_key and f.name.startswith("action") and getattr(skill, f.name) != 0]
        for a in actions:
            skill_utility.get_action_result(a)
        return actions


class UnitSummaryView(TemplateView):
    template_name = "pcrd_unpack/summary/unit_summary.html"

    def get_context_data(self, **kwargs):
        uss = models.UnitSummary.objects.all()
        context = {}
        context["data_tags"] = models.UnitSummary.data_tags()
        context["data_tags"].insert(1, 'position')

        context["unit_summary_data"] = {us:[int(getattr(us, p)) for p in context["data_tags"]]
                                        for us in uss}

        exp_team = models.ExperienceTeam.objects.all()
        exp_unit = models.ExperienceUnit.objects.all()
        skill_cost = models.SkillCost.objects.all()
        context["chart_datas"] = {
            'team' : {
                'title' : 'Player Experience',
                'labels': [exp_team[i].team_level for i in range(1, len(exp_team))],
                'data' : [exp_team[i].total_exp - exp_team[i-1].total_exp for i in range(1, len(exp_team))],
            },
            'unit' : {
                'title': 'Character Experience',
                'labels': [exp_unit[i].unit_level for i in range(1, len(exp_unit))],
                'data' : [exp_unit[i].total_exp - exp_unit[i-1].total_exp for i in range(1, len(exp_unit))],
            },
            'compare': {
                'title': 'Experience Food per Player Exp',
                'labels': [i.unit_level for i in exp_unit],
                'data': [(exp_unit[i].total_exp - exp_unit[i-1].total_exp) \
                         /(exp_team[i].total_exp - exp_team[i-1].total_exp)
                         for i in range(1, len(exp_unit))],
            },
            'skill_mana': {
                'title': 'skill mana per level',
                'labels': [i.target_level for i in skill_cost],
                'data': [skill_cost[i].cost
                         for i in range(1, len(skill_cost))],
            },
            'skill_compare': {
                'title': 'skill mana per player exp',
                'labels': [i.unit_level for i in exp_unit],
                'data': [(skill_cost[i].cost) \
                         / (exp_team[i].total_exp - exp_team[i - 1].total_exp)
                         for i in range(1, len(skill_cost))],
            },
        }
        add_max_info(context)
        return context

class IndexView(TemplateView):
    template_name = "pcrd_unpack/index.html"


def add_max_info(context:dict):
    context["max_level"] = models.UnitSummary.max_level()
    context["max_rank"] = models.UnitSummary.max_rank()
    context["max_rarity"] = models.UnitSummary.max_rarity()
    context["max_love"] = models.UnitSummary.max_love()
    return context



def handler404(request, exception=None):
    return HttpResponseNotFound(render_to_string('pcrd_unpack/errors/404.html', locals(), request))
