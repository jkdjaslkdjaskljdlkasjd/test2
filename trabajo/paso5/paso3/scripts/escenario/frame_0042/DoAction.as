// DoAction
// origen: escenario fotograma 42, DoAction (04083_DoAction.bin)

Krin.highestZoneDefeated = 0;
Krin.numberOfRespecUsed = 0;
Krin.numberOfTrainingUsed = 0;
Krin.topDamagePhysical = 0;
Krin.topDamageElemental = 0;
checkAndUpdateZoneAchievements = function()
{
   if(!(Krin.highestZoneDefeated < 1))
   {
      _root.sendAchievement("ACH_S2_BEAT_ZONE_1");
   }
   if(!(Krin.highestZoneDefeated < 2))
   {
      _root.sendAchievement("ACH_S2_BEAT_ZONE_2");
   }
   if(!(Krin.highestZoneDefeated < 3))
   {
      _root.sendAchievement("ACH_S2_BEAT_ZONE_3");
   }
   if(!(Krin.highestZoneDefeated < 4))
   {
      _root.sendAchievement("ACH_S2_BEAT_ZONE_4");
   }
   if(!(Krin.highestZoneDefeated < 5))
   {
      _root.sendAchievement("ACH_S2_BEAT_ZONE_5");
   }
   if(!(Krin.highestZoneDefeated < 6))
   {
      _root.sendAchievement("ACH_S2_BEAT_ZONE_6");
   }
   if(!(Krin.highestZoneDefeated < 7))
   {
      _root.sendAchievement("ACH_S2_BEAT_ZONE_7");
   }
};
updateSonny2AchByIndex = function(achId)
{
   var _loc3_ = ["ACH_S2_BEAT_ZONE_1", "ACH_S2_SOLO_CLEMONS", "ACH_S2_SUPPORT_HYDRA", "ACH_S2_BEAT_HUNT_CLEAN", "ACH_S2_BEAT_MAYOR_CLEAN", "ACH_S2_ALL_CLASSES", "ACH_S2_BEAT_WARDEN_DUO", "ACH_S2_TIME_BOMB_UNDER_40", "ACH_S2_SOLO_NOSTALGIA", "ACH_S2_BEAT_ZONE_7"];
   trace("Updating Original Sonny 2 Ach ID: " + achId);
   var _loc2_ = _loc3_[achId];
   _root.sendAchievement(_loc2_);
};
updateZoneDefeated = function(zoneId)
{
   trace("Updating Top Zone Defeated: " + zoneId);
   sendWrapperMessage("Updating Top Zone Defeated: " + zoneId);
   if(zoneId > Krin.highestZoneDefeated)
   {
      Krin.highestZoneDefeated = zoneId;
   }
};
updateTopPhysicalDamage = function(damage)
{
   trace("Updating Top Physical Damage: " + damage + " // Current Best: " + Krin.topDamagePhysical);
   if(damage > Krin.topDamagePhysical)
   {
      Krin.topDamagePhysical = damage;
   }
   if(!(damage < 2000))
   {
      _root.sendAchievement("ACH_S2_DEAL_X_PHYSICAL");
   }
};
updateTopElementalDamage = function(damage)
{
   trace("Updating Top Elemental Damage: " + damage + " // Current Best: " + Krin.topDamageElemental);
   if(damage > Krin.topDamageElemental)
   {
      Krin.topDamageElemental = damage;
   }
   if(!(damage < 2000))
   {
      _root.sendAchievement("ACH_S2_DEAL_X_ELEMENTAL");
   }
};
