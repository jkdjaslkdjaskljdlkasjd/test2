// ------------------------------------------------------------------------------- textos (lenguaje Krin)
// Todos los numeros salen de las mismas tablas que usa el combate. P(0.2025) = "20.25".
_root.__rwP = function(x)
{
   return _root.__rwPct(x) + "%";
};
// "235% of your Strength" o "245% of your Strength as Ice damage (343% of your Instinct if higher)"
_root.__rwScale = function(m, ice)
{
   var s = _root.__rwP(m) + " of your Strength";
   if(ice)
   {
      s += " as Ice damage (" + _root.__rwP(m * 1.4) + " of your Instinct if higher)";
   }
   return s;
};
_root.__rwScaleI = function(m)
{
   return _root.__rwP(m) + " of your Strength (" + _root.__rwP(m * 1.4) + " of your Instinct if higher)";
};
_root.__rwWoundPerText = function()
{
   var k = 1;
   var dw = _root.__rwRank(814);
   if(dw == 1)
   {
      k = 1.2;
   }
   if(dw > 1)
   {
      k = 1.35;
   }
   return _root.__rwP(0.15 * k);
};
_root.__rwDesc = function(id, r)
{
   var A = _root.__rwAt;
   var P = _root.__rwP;
   var wp = _root.__rwWoundPerText();
   var wt = _root.__rwWoundTurns();
   var wtxt = "'Wounds' (each bleeds for " + wp + " of your Strength per turn for " + wt + " turns)";
   if(id == 861)
   {
      var s = "Rake the enemy for " + _root.__rwScale(A([1.7, 2, 2.35], r)) + ". Inflicts " + A([2, 2, 3], r) + " " + wtxt;
      if(r == 2)
      {
         s += ", 1 more if it was already Wounded";
      }
      return s + ", and grants you 1 'Scent of Blood' on it (2 if it was already Wounded).";
   }
   if(id == 810)
   {
      return "Pounce on the enemy for " + _root.__rwScale(A([1.65, 1.9], r)) + ", dealing 30% more for each 'Scent of Blood' on it. Recovers " + A([8, 10], r) + " Focus per Scent and grants you 'Blood Rush': +5% direct damage for 3 turns, stacking up to 3 times (+15%).";
   }
   if(id == 812)
   {
      return "Cripple the enemy for " + _root.__rwScale(A([1.75, 2.05], r)) + ": -" + A([30, 40], r) + "% Speed for 2 turns. Inflicts 1 'Wound' and grants you 1 'Scent of Blood' (2 if it was already Wounded).";
   }
   if(id == 831)
   {
      var k = A([1.3, 1.5], r);
      return "Tear the enemy's wounds open for " + _root.__rwScale(A([1.5, 1.8], r)) + ". Every 'Wound' on it bursts at once for " + P(k) + " of the bleeding it had left and is consumed. Grants you 1 'Scent of Blood' for every 2 Wounds consumed. With 3 or more consumed, the target suffers 'Hemorrhage' for 2 turns: -20% Physical and Ice Defense, -15% damage dealt.";
   }
   if(id == 832)
   {
      return "Sink your fangs into your own flesh: lose 10% of your current Health and suffer 2 'Wounds' yourself (15% of your Strength per turn each, 3 turns). For 3 turns you are in 'Killer Instinct': +" + A([30, 40], r) + "% Strength and Instinct, +" + A([15, 20], r) + "% Speed, your attacks cannot be dodged, every ability that inflicts 'Wounds' inflicts 1 more, and you take 15% more damage. Recovers " + A([20, 25], r) + " Focus.";
   }
   if(id == 864)
   {
      var f = A([20, 30], r);
      return "Clamp down on the enemy for " + _root.__rwScale(A([2.8, 3.2], r)) + " and destroy " + f + " Focus (" + f * 2 + " against a Hunted target). For 2 turns it takes 15% more damage and has 25% less Speed. If it carries a 'Scent of Blood', consumes one: the target cannot use abilities that cost Focus for 2 turns.";
   }
   if(id == 819)
   {
      var s = "Execute the enemy for " + _root.__rwScale(A([2.6, 3, 3.4], r)) + ", +80% damage for each 'Scent of Blood' on it (consumed) and +25% for each 'Wound' on it (not consumed). Deals 40% more damage to targets below 35% Health.";
      if(r >= 3)
      {
         s += " Always a critical hit against a Brittle target.";
      }
      return s;
   }
   if(id == 863)
   {
      var s = "Unleash the howl of your ancestors for " + _root.__rwScale(A([1.8, 2.3, 2.8], r), true) + ", 100% stunned for 2 turns (also bosses)";
      var fb = A([0, 2, 3], r);
      if(fb > 0)
      {
         s += " and " + fb + " 'Frostbite'";
      }
      return s + ". Against 2 or more 'Scent of Blood', consumes 2: the target loses 25 Focus on each of its next 2 turns.";
   }
   if(id == 865)
   {
      return "Tear at the enemy with frozen claws for " + _root.__rwScale(A([1.85, 2.15, 2.45], r), true) + ". Applies " + A([1, 2, 2], r) + " 'Frostbite', +1 for every 2 'Wounds' on the target (up to +2), and -20% healing received for 3 turns.";
   }
   if(id == 815)
   {
      return "Bite the enemy with ancestral frost for " + _root.__rwScale(A([2, 2.3, 2.6], r), true) + ". Freezes up to " + (_root.__rwAspect() == 1 ? 7 : 3) + " 'Wounds' on it: each deals the bleeding it had left at once as Ice damage, is consumed and becomes 1 'Frostbite'.";
   }
   if(id == 816)
   {
      return "Shatter the frost on the enemy for " + _root.__rwScale(A([1.15, 1.45], r), true) + " for each 'Frostbite' on it (at least once), consuming them all. With 3 or more consumed, also dispels " + r + " beneficial effect" + (r > 1 ? "s" : "") + " and inflicts 1 'Wound' for every 2 Frostbite. You gain 1 'Ice Shard' for every 2 Frostbite consumed.";
   }
   if(id == 818)
   {
      return "Release a trail of frozen blood: " + _root.__rwScale(A([1.4, 1.6, 1.8], r), true) + " to all enemies, plus 1 'Frostbite' and 1 'Wound' on each. On Black Ice it applies 1 more 'Frostbite' and extends the ice by 1 turn.";
   }
   if(id == 833)
   {
      var per = A([0.15, 0.2], r);
      return "Coat the ground under the enemy team with black ice for " + A([2, 3], r) + " turns and scatter all your 'Ice Shards' on it. Every time an enemy acts on the ice it gains 1 'Frostbite' and takes " + _root.__rwScale(per, true) + " per Shard scattered.";
   }
   if(id == 862)
   {
      var b = A([18, 25], r);
      return "Awaken the instincts of an ally or yourself: +" + b + "% Strength, Instinct and Speed for 2 turns, +1 turn for every 2 'Wounds' on the most Wounded enemy (up to " + A([4, 5], r) + " turns). While it lasts, its direct attacks deal 5% more damage for each 'Wound' on the target (up to 25%).";
   }
   if(id == 834)
   {
      return "Let the pack feed for 3 turns: your allies' direct attacks deal " + A([6, 8], r) + "% more damage for each 'Wound' on the target (up to " + A([30, 40], r) + "%) and heal them for " + A([10, 15], r) + "% of the damage dealt.";
   }
   if(id == 835)
   {
      return "Share the ancestral frost with your allies for 3 turns: the first direct attack of each ally every turn applies 1 'Frostbite', and their attacks deal " + A([4, 6], r) + "% more damage for each 'Frostbite' on the target (up to " + A([20, 30], r) + "%).";
   }
   if(id == 821)
   {
      return "Rally an ally or yourself, healing for " + _root.__rwScaleI(A([2.6, 3.1, 3.6], r)) + " + " + A([10, 12, 15], r) + "% of its maximum Health, +10% for each 'Wound' and 'Frostbite' on the enemy team (up to +80%). Removes " + A([1, 1, 2], r) + " harmful effect" + (r > 2 ? "s" : "") + ", and its next direct attack deals " + A([15, 20, 25], r) + "% more damage (3 turns).";
   }
   if(id == 822)
   {
      return "Stand guard over an ally for 2 turns, shielding yourself for " + _root.__rwScaleI(A([1.7, 2.2], r)) + ". The shield absorbs " + A([30, 40], r) + "% of the direct damage your ally takes, and each enemy that strikes your ally gains 1 'Frostbite'. Consumes up to 2 'Scent of Blood' from the most marked enemy: +35% shield and +1 turn each.";
   }
   if(id == 824)
   {
      return "Let the pack's howl echo, shielding every ally, you included, for " + _root.__rwScaleI(A([1.3, 1.65, 2], r)) + " for 2 turns. Enemies that strike a shielded ally suffer 1 'Wound'. Consumes up to 2 'Scent of Blood' from the target.";
   }
   if(id == 808)
   {
      var s = "Share the primal breath of the pack for 3 turns: every ally, you included, instantly recovers " + A([15, 20], r) + " Focus, then " + A([10, 15], r) + " Focus per turn, gains " + A([15, 20], r) + "% Speed and takes " + A([8, 10], r) + "% less damage.";
      if(r > 1)
      {
         s += " Also removes 1 harmful effect from each ally.";
      }
      return s + " Consumes up to 2 'Scent of Blood' from the most marked enemy: +1 turn each.";
   }
   if(id == 809)
   {
      return "Morph into an undead beast for 3 turns: +" + A([25, 35], r) + "% Strength and Instinct, and you recover " + A([8, 12], r) + "% of your maximum Health per turn. While transformed, your direct attacks inflict 1 'Wound'.";
   }
   if(id == 826)
   {
      var s = "Catch your second wind, healing " + A([10, 15], r) + "% of your maximum Health. Drinks up to 3 'Wounds' from the most Wounded enemy: +" + A([15, 20], r) + "% of your maximum Health for each (up to " + A([55, 75], r) + "%).";
      if(r > 1)
      {
         s += " Also removes 1 harmful effect.";
      }
      return s;
   }
   if(id == 836)
   {
      return "Bite the enemy for " + _root.__rwScale(A([1.8, 2.1], r)) + " and drink 1 'Wound' from it, healing yourself for " + A([60, 80], r) + "% of the damage dealt + 5% of your maximum Health for each Wound it still carries.";
   }
   if(id == 827)
   {
      return "Make a last stand for 1 turn: -" + A([55, 70], r) + "% damage taken and -" + A([25, 20], r) + "% damage dealt. Consumes every 'Scent of Blood' on the most marked enemy: 5% less damage taken for each (up to 85%).";
   }
   if(id == 837)
   {
      return "Coat your fur in rime for 3 turns: -" + A([15, 25], r) + "% damage taken, and each enemy that strikes you with a direct attack gains 1 'Frostbite'. Consumes up to 3 'Ice Shards': 5% less damage taken for each (up to 40%).";
   }
   if(id == 838)
   {
      return "Encase an ally or yourself in ancestral ice for 1 turn: 100% stunned (loses its next turn), -90% damage taken, and cleansed of every harmful effect. When the ice breaks, it heals 15% of its maximum Health.";
   }
   if(id == 857)
   {
      var s = "Bite the enemy with a frozen maw for " + _root.__rwScale(_root.__rwMawMult(), true) + " (160% at Lvl. 1, up to 240% at Lvl. 20). Applies 1 'Frostbite' and recovers 5 Focus (10 against a Brittle target).";
      if(_root.__rwNum(_root.Krin.Level) >= 10)
      {
         s += " (Lvl. 10) Against a Brittle target, applies 2 'Frostbite'.";
      }
      return s;
   }
   if(id == 854)
   {
      return "Raise the blood moon for 3 turns. At the start of each of their turns, every enemy suffers 1 'Wound'. Your Wounds deal their damage twice and heal you for 30% of it. When the moon sets, every Wound on every enemy bursts at once for 100% of the bleeding it had left.";
   }
   if(id == 855)
   {
      return "Call an endless winter for 3 turns. At the start of each of their turns, every enemy gains 2 'Frostbite' and has 30% less Speed. You gain 5 'Ice Shards' and they do not expire while it lasts. Enemies frozen solid stay frozen for 2 turns (1 against bosses). When the winter ends, all Frostbite shatters for " + _root.__rwScale(0.6, true) + " per stack.";
   }
   if(id == 856)
   {
      return "Call your ancestors to take your body for 3 turns ('Ancestral Form'): you deal 100% more damage, direct and over time, and take 25% less. Heals 65% of your maximum Health, recovers all your Focus, and you act again at once. The ally with the lowest Health receives 'Ancestors' Blessing' for 3 turns: if it falls, an ancestral wolf takes its place.";
   }
   // ---- instintos
   if(id == 811)
   {
      var s = "Passive. Each enemy can carry up to " + A([2, 3], r) + " 'Scent of Blood' (3 turns; a new Scent refreshes them). A Wound ticking on a frostbitten enemy grants you 1 Scent.";
      if(r > 1)
      {
         s += " At 3 Scents the enemy is Hunted for 2 turns: +15% damage received from your team, cannot dodge your attacks, -25% healing received.";
      }
      return s + " Awakens Ancestral Wolf.";
   }
   if(id == 814)
   {
      var s = "Passive. Enemies can carry up to 5 'Wounds' instead of 3. Your Wounds deal " + A([20, 35], r) + "% more damage (" + P(0.15 * A([1.2, 1.35], r)) + " of your Strength per Wound each turn)";
      if(r > 1)
      {
         s += " and last 4 turns. When a Wounded enemy dies, its Wounds burst: every other enemy takes 50% of the bleeding it had left";
      }
      return s + ".";
   }
   if(id == 817)
   {
      return "Passive. You gain " + A([7, 10], r) + "% Physical and Ice Piercing for each 'Scent of Blood' on your target (up to " + A([21, 30], r) + "%).";
   }
   if(id == 839)
   {
      return "Passive. Each time a Wounded enemy acts, it loses " + A([2, 3], r) + " Focus for each 'Wound' it carries (up to 15).";
   }
   if(id == 820)
   {
      var s = "Passive. You recover " + A([6, 9], r) + " Focus for each 'Scent of Blood' or 'Frostbite' you consume";
      if(r > 1)
      {
         s += ", and 15 Focus whenever an enemy becomes Hunted or is frozen solid";
      }
      return s + ".";
   }
   if(id == 840)
   {
      var s = "Passive. You can hold up to " + A([3, 5], r) + " 'Ice Shards' (2 without this passive). Each Shard reduces the damage you take by 3% and recovers 2 Focus per turn. You gain Shards when you consume Frostbite (Shatter Guard) or freeze an enemy solid (+2).";
      if(r > 1)
      {
         s += " While you hold 3 or more, enemies that strike you with a direct attack gain 1 'Frostbite'.";
      }
      return s;
   }
   if(id == 841)
   {
      return "Passive. Your 'Wounds' deal " + A([6, 10], r) + "% more damage for each 'Frostbite' on the target (up to " + A([30, 50], r) + "%).";
   }
   if(id == 842)
   {
      return "Passive. An enemy that thaws out of Frozen Solid keeps " + A([1, 2], r) + " 'Frostbite'.";
   }
   if(id == 843)
   {
      var s = "Passive. The first time each turn an enemy becomes Brittle, it loses " + A([10, 15], r) + " Focus";
      if(r > 1)
      {
         s += " and takes " + _root.__rwScale(0.6, true);
      }
      return s + ".";
   }
   if(id == 823)
   {
      var s = "Passive. Your allies deal " + A([2, 3], r) + "% more damage for each 'Wound' on their target (up to " + A([10, 15], r) + "%).";
      if(r > 1)
      {
         s += " Their attacks against a Hunted target heal them for 15% of the damage dealt.";
      }
      return s;
   }
   if(id == 844)
   {
      return "Passive. Whenever your 'Wounds' deal damage, the ally with the lowest Health (you included) is healed for " + A([20, 30], r) + "% of it.";
   }
   if(id == 845)
   {
      return "Passive. Your allies take " + A([2, 3], r) + "% less damage from an enemy for each 'Frostbite' it carries (up to " + A([10, 15], r) + "%).";
   }
   if(id == 825)
   {
      return "Passive. +" + A([18, 28], r) + "% Physical and Ice Defense, and you take " + A([8, 12], r) + "% less damage.";
   }
   if(id == 846)
   {
      return "Passive. You heal for " + A([15, 25], r) + "% of the damage your 'Wounds' deal.";
   }
   if(id == 828)
   {
      var s = "Passive. You take " + A([15, 25], r) + "% less damage from damage over time";
      if(r > 1)
      {
         s += " and recover 5 Focus per turn";
      }
      return s + ". Consuming a 'Wound' removes one damage-over-time effect from you.";
   }
   if(id == 829)
   {
      var s = "Passive. Each 'Wound' or 'Frostbite' you consume shields you for " + A([7, 10], r) + "% of your maximum Health (up to " + A([35, 40], r) + "%) for 2 turns.";
      if(r > 1)
      {
         s += " You also receive 15% more healing.";
      }
      return s;
   }
   if(id == 830)
   {
      return "Passive. Once per battle, a blow that would kill you leaves you at 25% of your maximum Health, shielded for a further 20% for 2 turns, and free of every harmful effect.";
   }
   return "";
};
// maestrias (rango maximo)
_root.__rwStarText = function(id)
{
   if(id == 861)
   {
      return "Against a Hunted target, inflicts 1 more 'Wound' and its Wounds last 5 turns.";
   }
   if(id == 810)
   {
      return "At 3 stacks of 'Blood Rush', also inflicts 1 'Wound' and grants you 1 'Scent of Blood'.";
   }
   if(id == 812)
   {
      return "A Hunted target slower than you also loses its next turn (100% stunned for 1 turn). Once every 4 turns.";
   }
   if(id == 831)
   {
      return "Consuming 5 or more Wounds makes the Hemorrhage last 3 turns and leaves the target 'Torn': +20% damage received for 2 turns.";
   }
   if(id == 832)
   {
      return "Each enemy you kill while it lasts extends it by 1 turn and heals you for 15% of your maximum Health.";
   }
   if(id == 864)
   {
      return "Consuming the Scent also returns 25 Focus to you.";
   }
   if(id == 819)
   {
      return "If the target dies, the Focus is refunded and its Wounds jump to the enemy with the lowest Health.";
   }
   if(id == 863)
   {
      return "If it consumed 2 Scents, every other enemy gains 1 'Frostbite' and loses 15 Focus.";
   }
   if(id == 865)
   {
      return "Against a Brittle target, strikes a second time for 60% of the damage and applies 1 more 'Frostbite'.";
   }
   if(id == 815)
   {
      return "If this freezes the target solid, you recover 20 Focus and the Wounds are not consumed.";
   }
   if(id == 816)
   {
      return "If 5 or more Frostbite are consumed, the target becomes 'Fragile': +25% damage received for 3 turns.";
   }
   if(id == 818)
   {
      return "Enemies that already had Frostbite gain 1 more 'Frostbite', and enemies that already had Wounds gain 2 'Wounds' instead of 1.";
   }
   if(id == 833)
   {
      return "An enemy frozen solid on the ice shatters for " + _root.__rwScale(1.5, true) + " and returns 2 'Ice Shards' to you.";
   }
   if(id == 862)
   {
      return "Every other ally, you included, gains half the bonus: +12.5% Strength, Instinct and Speed for 3 turns.";
   }
   if(id == 834)
   {
      return "Against a target with 5 or more Wounds, an ally's attack consumes 1 Wound to deal 50% more damage.";
   }
   if(id == 835)
   {
      return "Allies' critical hits against a Brittle target apply 2 'Frostbite' instead of 1.";
   }
   if(id == 821)
   {
      return "An ally below 30% Health is healed a second time for 50% of the amount.";
   }
   if(id == 822)
   {
      return "When the shield breaks, you strike the attacker for 120% of your Strength and inflict 2 'Wounds'.";
   }
   if(id == 824)
   {
      return "Each Scent consumed applies 2 'Frostbite' to the target.";
   }
   if(id == 808)
   {
      return "When it ends, each ally heals 15% of its maximum Health and deals 15% more damage for 2 turns.";
   }
   if(id == 809)
   {
      return "Each 'Scent of Blood' you consume while transformed extends it by 1 turn (up to 2) and heals you for 5% of your maximum Health.";
   }
   if(id == 826)
   {
      return "If it drinks 3 Wounds, removes every harmful effect from you.";
   }
   if(id == 836)
   {
      return "Against a Hunted target it drinks no Wound and heals you for 100% of the damage dealt.";
   }
   if(id == 827)
   {
      return "Enemies that strike you meanwhile gain 2 'Frostbite'; a Brittle attacker is frozen solid instead.";
   }
   if(id == 837)
   {
      return "An enemy frozen solid by Rime Coat takes " + _root.__rwScale(1.5, true) + ".";
   }
   if(id == 838)
   {
      return "When the ice breaks, every enemy gains 1 'Frostbite'.";
   }
   if(id == 811)
   {
      return "Becoming Hunted also inflicts 2 'Wounds'.";
   }
   if(id == 814)
   {
      return "Your Wounds deal 50% more damage to Hunted targets and cannot be dispelled from them.";
   }
   if(id == 817)
   {
      return "Your critical hits inflict 1 'Wound'.";
   }
   if(id == 839)
   {
      return "An enemy below 20 Focus is 'Terrified': -20% damage dealt, and each of your attacks against it recovers 5 Focus.";
   }
   if(id == 820)
   {
      return "When an enemy becomes Hunted or is frozen solid, all your cooldowns drop by 1 turn.";
   }
   if(id == 840)
   {
      return "Holding 5 Shards makes your Ice attacks ignore 20% of the target's Ice Defense.";
   }
   if(id == 841)
   {
      return "A target frozen solid keeps bleeding, and its Wounds deal their damage twice while it is frozen.";
   }
   if(id == 842)
   {
      return "Enemies that are not bosses stay frozen solid for 2 turns instead of 1.";
   }
   if(id == 843)
   {
      return "Becoming Brittle also inflicts 1 'Wound'.";
   }
   if(id == 823)
   {
      return "Your allies' attacks against a Hunted target restore 5 Focus to you (once per ally each turn).";
   }
   if(id == 844)
   {
      return "Healing above maximum Health becomes a shield worth up to 15% of the ally's maximum Health for 2 turns.";
   }
   if(id == 845)
   {
      return "When an enemy is frozen solid, every ally, you included, recovers 10 Focus.";
   }
   if(id == 825)
   {
      return "While any enemy carries Frostbite, you take a further 10% less damage.";
   }
   if(id == 846)
   {
      return "Healing above your maximum Health becomes a shield worth up to 20% of it for 2 turns.";
   }
   if(id == 828)
   {
      return "Consuming 3 or more Wounds in one action makes you immune to stuns for 1 turn.";
   }
   if(id == 829)
   {
      return "Freezing an enemy solid shields you for 15% of your maximum Health.";
   }
   if(id == 830)
   {
      return "Whatever struck that blow takes 3 'Scent of Blood', 3 'Frostbite' and 3 'Wounds'.";
   }
   return "";
};
// texto completo de una habilidad al rango r (con la maestria si r es el maximo)
_root.__rwFullDesc = function(id, r)
{
   var d = _root.__rwS[id];
   var s = _root.__rwDesc(id, r);
   if(d && d.pg > 0 && d.pg < 3 && r >= d.max)
   {
      var m = _root.__rwStarText(id);
      if(m != "")
      {
         s += "  ★ Mastery: " + m;
      }
   }
   return s;
};
// Aspectos
_root.__rwAspectText = function(k)
{
   if(k == 1)
   {
      return "Passive Aspect. Enemies can carry up to 7 'Wounds', and Rupture and Frost Fang consume up to 7. Every 'Frostbite' you apply is reduced by 1 (minimum 1). Unlocks Blood Moon Rising.";
   }
   if(k == 2)
   {
      return "Passive Aspect. Enemies can carry up to 7 'Frostbite' (the 8th freezes them solid), Brittle adds 30% damage instead of 20%, and Shatter Guard counts up to 7. Your 'Wounds' last 1 turn less. Unlocks Endless Winter.";
   }
   if(k == 3)
   {
      return "Passive Aspect. For the whole battle your allies gain 10% Strength, Instinct and Speed, and you deal 15% less direct damage.";
   }
   if(k == 4)
   {
      return "Passive Aspect. Once per battle, when you fall below 40% Health, the ancestors take your body for 3 turns ('Ancestral Form'): +40% damage dealt, -25% damage taken, 100% immune to stuns. When it ends you are 'Spent': -20% damage dealt for 2 turns. Unlocks Call of the Ancestors.";
   }
   return "";
};
// estados: textos de los iconos de combate (se pintan con numeros exactos)
_root.__rwStatusText = function(u, id)
{
   var P = _root.__rwP;
   if(id == "RWWOUND" || id == "RWWOUNDH")
   {
      var W = _root.__rwWounds(u);
      var per = _root.__rwWoundPer(u);
      var w = _root.__rwWolf();
      var base = _root.__rwNum(w.STRENGTHU);
      var pc = base > 0 ? per / base : 0.15;
      // en el tooltip de estado, porcentajes enteros (30% y no 30.38%)
      var s = "Bleeds for " + Math.round(pc * W * 100) + "% of the wolf's Strength per turn (" + Math.round(pc * 100) + "% per Wound) as Physical damage. " + W + " of " + _root.__rwWoundCap() + " Wounds.";
      if(id == "RWWOUNDH")
      {
         s += " Cannot be dispelled.";
      }
      return s;
   }
   if(id.substr(0, 7) == "RWFROST")
   {
      var n = _root.__rwFrost(u);
      var s = "-" + 4 * n + "% Speed, -" + 3 * n + "% damage dealt.";
      if(n >= 3)
      {
         s += " Brittle: +" + (_root.__rwAspect() == 2 ? 30 : 20) + "% damage received from the wolf's attacks.";
      }
      return s + " 1 more Frostbite at " + _root.__rwFrostCap() + " freezes it solid.";
   }
   if(id == "RWSCENT")
   {
      return "Marked by the wolf: " + _root.__rwScent(u) + " of " + _root.__rwScentCap() + " Scents. At 3 it becomes Hunted.";
   }
   if(id == "RWHUNTED")
   {
      return "+15% damage received from the wolf's team, cannot dodge the wolf's attacks, -25% healing received.";
   }
   if(id == "RWSOLID")
   {
      return "100% stunned: loses its turn. Frostbite reset to 0.";
   }
   if(id == "RWFRAGILE")
   {
      return "+25% damage received.";
   }
   if(id == "RWHEMO")
   {
      return "-20% Physical and Ice Defense, -15% damage dealt.";
   }
   if(id == "RWTORN")
   {
      return "+20% damage received.";
   }
   if(id == "RWSILENCE")
   {
      return "Cannot use abilities that cost Focus.";
   }
   if(id == "RWSTUN" || id == "RWCRIPPLE")
   {
      return "100% stunned: loses its turn.";
   }
   if(id == "RWDREAD")
   {
      return "Loses 25 Focus each turn.";
   }
   if(id == "RWHAM1" || id == "RWHAM2")
   {
      return "-" + (id == "RWHAM2" ? 40 : 30) + "% Speed.";
   }
   if(id == "RWJAWS")
   {
      return "+15% damage received, -25% Speed.";
   }
   if(id == "RWWICKED")
   {
      return "-20% healing received.";
   }
   if(id == "RWBLACKICE")
   {
      return "Each time it acts: +1 Frostbite and damage for each of the " + _root.__rwNum(u.__rwIceShards) + " Ice Shards scattered.";
   }
   if(id == "RWTERROR")
   {
      return "-20% damage dealt while below 20 Focus. The wolf recovers 5 Focus each time it strikes it.";
   }
   if(id == "RWWSLOW")
   {
      return "-30% Speed.";
   }
   if(id.substr(0, 6) == "RWRUSH")
   {
      return "+" + 5 * Number(id.substr(6, 1)) + "% direct damage.";
   }
   if(id == "RWKILLER1" || id == "RWKILLER2")
   {
      var b = id == "RWKILLER2" ? 40 : 30;
      var sp = id == "RWKILLER2" ? 20 : 15;
      return "+" + b + "% Strength and Instinct, +" + sp + "% Speed, attacks cannot be dodged, +1 Wound per wounding ability, +15% damage received.";
   }
   if(id == "RWSHARD")
   {
      var S = _root.__rwShards(u);
      var s = S + " of " + _root.__rwShardCap() + " Shards: -" + 3 * S + "% damage taken";
      if(_root.__rwRank(840) > 0)
      {
         s += ", +" + 2 * S + " Focus per turn";
      }
      return s + ".";
   }
   if(id == "RWRIME")
   {
      return "-" + Math.round(_root.__rwNum(u.__rwRimeRed) * 100) + "% damage taken. Direct attackers gain 1 Frostbite.";
   }
   if(id == "RWTOMB")
   {
      return "100% stunned, -90% damage taken. Heals 15% of maximum Health when the ice breaks.";
   }
   if(id == "RWCANINE1" || id == "RWCANINE2" || id == "RWCANINEH")
   {
      var v = id == "RWCANINE2" ? "25" : (id == "RWCANINE1" ? "18" : "12.5");
      var s = "+" + v + "% Strength, Instinct and Speed.";
      if(id != "RWCANINEH")
      {
         s += " Direct attacks: +5% damage per Wound on the target (up to 25%).";
      }
      return s;
   }
   if(id == "RWFRENZY")
   {
      var fr = _root.__rwNum(u.__rwFrenzyR);
      return "Direct attacks: +" + (fr > 1 ? 8 : 6) + "% damage per Wound on the target (up to " + (fr > 1 ? 40 : 30) + "%), heal " + (fr > 1 ? 15 : 10) + "% of the damage dealt.";
   }
   if(id == "RWFROSTPACK")
   {
      var fp = _root.__rwNum(u.__rwFrostPackR);
      return "First direct attack each turn: +1 Frostbite. +" + (fp > 1 ? 6 : 4) + "% damage per Frostbite on the target (up to " + (fp > 1 ? 30 : 20) + "%).";
   }
   if(id == "RWCOURAGE")
   {
      return "Next direct attack: +" + Math.round(_root.__rwNum(u.__rwCourage) * 100) + "% damage.";
   }
   if(id == "RWGUARD")
   {
      return "Guarded by the wolf: " + Math.round(_root.__rwNum(u.__rwGuardShare) * 100) + "% of the direct damage it takes goes to the wolf's shield. Attackers gain 1 Frostbite.";
   }
   if(id == "RWPRIMAL1" || id == "RWPRIMAL2")
   {
      var two = id == "RWPRIMAL2";
      return "+" + (two ? 15 : 10) + " Focus per turn, +" + (two ? 20 : 15) + "% Speed, -" + (two ? 10 : 8) + "% damage taken.";
   }
   if(id == "RWPRIMALEND")
   {
      return "+15% damage dealt.";
   }
   if(id == "RWWERE1" || id == "RWWERE2")
   {
      var two = id == "RWWERE2";
      return "+" + (two ? 35 : 25) + "% Strength and Instinct, recovers " + (two ? 12 : 8) + "% of maximum Health per turn. Direct attacks inflict 1 Wound.";
   }
   if(id == "RWSTAND1" || id == "RWSTAND2")
   {
      return "-" + Math.round(_root.__rwNum(u.__rwStandRed) * 100) + "% damage taken, -" + (id == "RWSTAND2" ? 20 : 25) + "% damage dealt.";
   }
   if(id == "RWANCFORM")
   {
      return "+40% damage dealt, -25% damage taken, 100% immune to stuns.";
   }
   if(id == "RWCALL")
   {
      return "+100% damage dealt (direct and over time), -25% damage taken.";
   }
   if(id == "RWSPENT")
   {
      return "-20% damage dealt.";
   }
   if(id == "RWBLESS")
   {
      return "If it falls, an ancestral wolf takes its place.";
   }
   if(id == "RWSPIRIT")
   {
      return "An ancestral wolf that took a fallen ally's place.";
   }
   if(id == "RWBMOON")
   {
      return "Enemies suffer 1 Wound at the start of each of their turns. Wounds deal their damage twice and heal the wolf for 30% of it. Every Wound bursts when it ends.";
   }
   if(id == "RWEWINTER")
   {
      return "Enemies gain 2 Frostbite and -30% Speed at the start of each of their turns. Ice Shards do not expire. All Frostbite shatters when it ends.";
   }
   if(id == "RWSTUNIMM")
   {
      return "100% immune to stuns.";
   }
   if(id.substr(0, 5) == "RWSH_")
   {
      return "Shield: absorbs " + Math.round(_root.__rwNum(u.SHIELD)) + " damage.";
   }
   return "";
};

// descripcion vieja (__v55Desc): la usa el script de los iconos del lobo en la reserva y en la barra de combate.
// Para las habilidades del rework devuelve el texto nuevo del rango actual.
_root.__rwPrevDesc55 = _root.__v55Desc;
_root.__v55Desc = function(id, r)
{
   if(_root.__rwS[id])
   {
      return _root.__rwFullDesc(id, Math.max(1, _root.__rwRank(id)));
   }
   return _root.__rwPrevDesc55(id, r);
};
