const getStatusColor = (status) => {
  switch (status) {
    case "CRASHED":
      return "red";
    case "PARCEL_DELIVERED":
      return "green";
    default:
      return "blue";
  }
};

export { getStatusColor };
